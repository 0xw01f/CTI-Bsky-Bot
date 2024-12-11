#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By w01f : Original by JMousqueton, modified for Bluesky
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports 
# ---------------------------------------------------------------------------
import feedparser
import time
from datetime import datetime
import csv
import sys
from configparser import ConfigParser
import os
from os.path import exists
from optparse import OptionParser
from atproto import Client
import schedule
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Function to send Bluesky post 
# ---------------------------------------------------------------------------
def Send_Bluesky(content: str, url: str = None) -> bool:
    """
    Send a post to Bluesky
    Returns True if successful, False otherwise
    """
    try:
        # Create facets for URL if provided
        content_bytes = content.encode('utf-8')  # Get bytes of content
        url_bytes = url.encode('utf-8')         # Get bytes of URL

        facets = [{
            "index": {
                "byteStart": len(content_bytes) + 1, 
                "byteEnd": len(content_bytes) + 1 + len(url_bytes)
            },
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}]
        }]

        print(f"Content bytes: {len(content_bytes)}, URL bytes: {len(url_bytes)}")
        print(f"Facets: {facets}")


        # Create the post
        agent.send_post(text=f"{content}\n{url}" if url else content, facets=facets)
        return True
    except Exception as e:
        print(f"Error posting to Bluesky: {str(e)}")
        return False

# ---------------------------------------------------------------------------
# Add nice Emoji in front of title   
# ---------------------------------------------------------------------------
def Emoji(feed):
    # Nice emoji :) 
    match feed:
        case "Leak-Lookup":
            Title = '💧 '
        case "VERSION":
            Title = '🔥 '
        case "DataBreaches":
            Title = '🕳 '
        case "FR-CERT Alertes" | "FR-CERT Avis":
            Title = '🇫🇷 '
        case "EU-ENISA Publications":
            Title = '🇪🇺 '
        case "Cyber-News":
            Title = '🕵🏻‍♂️ '
        case "Bleeping Computer":
            Title = '💻 '
        case "Microsoft Sentinel":
            Title = '🔭 '
        case "Hacker News":
            Title = '📰 '
        # [Original emoji matches preserved...]
        case _:
            Title = '📢 '
    return Title

# ---------------------------------------------------------------------------
# Function fetch RSS feeds  
# ---------------------------------------------------------------------------
def GetRssFromUrl(RssItem):
    NewsFeed = feedparser.parse(RssItem[0])
    DateActivity = ""

    for RssObject in reversed(NewsFeed.entries):
        try:
            DateActivity = time.strftime('%Y-%m-%dT%H:%M:%S', RssObject.published_parsed)
        except: 
            DateActivity = time.strftime('%Y-%m-%dT%H:%M:%S', RssObject.updated_parsed)
        
        try:
            TmpObject = FileConfig.get('Rss', RssItem[1])
        except:
            FileConfig.set('Rss', RssItem[1], " = ?")
            TmpObject = FileConfig.get('Rss', RssItem[1])

        if TmpObject.endswith("?"):
            FileConfig.set('Rss', RssItem[1], DateActivity)
        else:
            if(TmpObject >= DateActivity):
                continue

        Title = Emoji(RssItem[1])
        Title += " " + RssObject.title

        if RssItem[1] == "VERSION":
                Title ='🔥 A NEW VERSION IS AVAILABLE : ' + RssObject.title
       
        if options.Debug:
            print(Title + " : " + RssObject.title + " (" + DateActivity + ")")
        else:
            Send_Bluesky(Title, RssObject.link)
            time.sleep(3)
        
        FileConfig.set('Rss', RssItem[1], DateActivity)

    with open(ConfigurationFilePath, 'w') as FileHandle:
        FileConfig.write(FileHandle)

# ---------------------------------------------------------------------------
# Log  
# ---------------------------------------------------------------------------
def CreateLogString(RssItem):
    LogString = "[*]" + time.ctime()
    LogString += " " + "checked " + RssItem
    if not options.Quiet: 
        print(LogString)
    time.sleep(2) 

# ---------------------------------------------------------------------------
# Main function to run feed checks
# ---------------------------------------------------------------------------
def check_feeds():
    with open('Feed.csv', newline='') as f:
        reader = csv.reader(f)
        RssFeedList = list(reader)
            
    for RssItem in RssFeedList:
        if '#' in str(RssItem[0]):
            continue
        GetRssFromUrl(RssItem)
        CreateLogString(RssItem[1])

# ---------------------------------------------------------------------------
# Main   
# ---------------------------------------------------------------------------    
if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 2.2.0")
    parser.add_option("-q", "--quiet",
                      action="store_true",
                      dest="Quiet",
                      default=False,
                      help="Quiet mode")
    parser.add_option("-D", "--debug",
                      action="store_true", 
                      dest="Debug",
                      default=False,
                      help="Debug mode : only output on screen nothing send to Bluesky")
    (options, args) = parser.parse_args()

    # Get Bluesky credentials from environment
    username = os.getenv('BLUESKY_USERNAME')
    password = os.getenv('BLUESKY_PASSWORD')

    if not username or not password:
        sys.exit("Please set BLUESKY_USERNAME and BLUESKY_PASSWORD environment variables")

    # Initialize Bluesky client
    agent = Client()
    agent.login(username, password)

    # Configuration file path
    ConfigurationFilePath = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'Config.txt')

    # Make some simple checks before starting 
    if sys.version_info < (3, 10):
        sys.exit("Please use Python 3.10+")
    if not exists(ConfigurationFilePath):
        sys.exit("Please add a Config.txt file")
    if not exists("./Feed.csv"):
        sys.exit("Please add the Feed.cvs file")
    
    # Read the Config.txt file   
    FileConfig = ConfigParser()
    FileConfig.read(ConfigurationFilePath)

    # Schedule the job to run every 3 hours
    schedule.every(3).hours.do(check_feeds)
    
    # Run once immediately
    check_feeds()

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)