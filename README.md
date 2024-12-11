
# 🏴‍☠️🤖 Threat Intelligence Bluesky Bot

The **Threat Intelligence Bluesky Bot** is a fork of the [original Threat Intelligence Teams Bot](https://github.com/JMousqueton/CTI-MSTeams-Bot) created by **Julien Mousqueton**. This bot now publishes threat intelligence updates on **Bluesky** instead of Microsoft Teams, and is designed to run periodically to check for new updates from various cybersecurity sources.

> The bot fetches updates from various clearnet domains, ransomware threat actor domains, and other cybersecurity-related feeds. It checks for new updates every 30 minutes and posts them on **Bluesky**.

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) ![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)  

## Description

* Written in Python
  - ⚠️ Requires Python 3.10+ for compatibility
* Posts to **Bluesky**
* Fetches updates from threat intelligence feeds (including clearnet domains, ransomware, and other cybersecurity sources)
* Checks for updates every 30 minutes

---

## Installation

Clone the repository or download the [latest release](https://github.com/JMousqueton/CTI-MSTeams-Bot/releases/latest)

```bash
git clone https://github.com/JMousqueton/CTI-Bluesky-Bot
```

Install all the required dependencies from `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

---

## Configuration

### Setup Environment Variables

Create a `.env` file in the project directory and add your **Bluesky credentials**:

```text
BLUESKY_USERNAME=your_username
BLUESKY_PASSWORD=your_password
```

This file will be used to securely load your credentials when the bot runs.

### On a server (Windows, macOS, Linux)

Make sure to set the appropriate environment variables:

```bash
BLUESKY_USERNAME=your_username
BLUESKY_PASSWORD=your_password
```

---

## Usage

Run the bot using the following command:

```bash
python3 blueskyBot.py -h
Usage: blueskyBot.py [options]

Options:
  --version       Show program's version number and exit
  -h, --help      Show this help message and exit
  -q, --quiet     Quiet mode (suppress output)
  -D, --debug     Debug mode: Only output on screen, no posts sent to Bluesky
```

---

## Adding or Removing RSS Feeds to Monitor

All monitored RSS feeds are listed in the `Feed.csv` file. To add a new RSS feed, simply append the URL and the name:

```text
https://example.com/feed/,Example Source
```

---

## Sources

This bot supports the following sources:

- 🇫🇷 **FR-CERT Avis** (ANSSI): Notifications from the French government CERT.
- 🇫🇷 **FR-CERT Alertes** (ANSSI): Alerts from the French government CERT.
- **Leak-lookup**: Leak notifications.
- **Cyber-News**: Cybersecurity news updates.
- **ATT CyberSecurity Blog**: Ransomware and security news.
- **EU-ENISA Publications**: European cybersecurity publications.
- **NCC Group**: Cyber threat intelligence reports.
- **Microsoft Sentinel**: Threat intelligence reports from Microsoft.
- **SANS**: Security and cybersecurity news.
- **Red Flag Domains**: Domains associated with cyber threats (use `-d` flag to enable).

---

## ToDo

- Enhance the bot with additional custom sources or features.

---

## Credit

This project was initially created by **Julien Mousqueton**. I have modified it to fit my own use case, switching the integration from Microsoft Teams to **Bluesky**. Special thanks to Julien for the original work and to everyone who has supported and contributed to this project.

Thanks also to the cybersecurity community for providing the threat intelligence feeds that make this bot useful.

---
