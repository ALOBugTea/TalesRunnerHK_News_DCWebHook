# TalesRunnerHK_News_DCWebHook
TalesRunnerHK_News_DCWebHook is used for catch [website](www.talesrunner.com.hk)'s game announcements, and post the html data with discord webhook on discord
>website link is www.talesrunner.com.hk
# Getting Started
## Requirements
- Python 3.11.0 (https://www.python.org/)
- Additional library listed in requirements.txt
## Installation
To run TalesRunnerHK_News_DCWebHook, you need python and install the library in requirements.txt with pip
```
pip install -r requirements.txt
```
>requirements.txt
```
beautifulsoup4==4.11.2
discord_webhook==1.1.0
requests==2.28.2
```
## Configuration
Open the file "trmsg_page_parser.py", the top can find the 'webhook_links'
```py
webhook_links = []
```
Insert your discord webhook link in brackets, like:
```py
webhook_links = [ 'https://discordapp.com/api/webhooks/...']
```
If you have more than one link, you can put them with comma:
```py
webhook_links = [ 'https://discordapp.com/api/webhooks/...',
                  'https://discordapp.com/api/webhooks/...'
                ]
```
## Usage
run this comma in cmd
```
py trmsg_page_parser.py
```

## How it works?
Get string data from trmsg_titles.txt, get requests with three links from 
- 官網公告欄 'https://www.talesrunner.com.hk/news/MMXIII_news.html'
- 最新消息 'https://www.talesrunner.com.hk/notice/notice.php?type=system'
- 更新情報 'https://www.talesrunner.com.hk/notice/notice.php?type=patch'
>官網公告欄's encoding is using big5, 最新情報 and 更新情報 is UTF-8

Using Soup to get id "allNoticeContainer" in 官網公告欄, can find
- event type
- event link
- event's picture bar

If type is 最新消息 or 更新情報, find the td pointer, get the previous and next siblings with a limit count

Post the msg with discord webhook.

