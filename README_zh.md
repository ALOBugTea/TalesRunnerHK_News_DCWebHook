# TalesRunnerHK_News_DCWebHook
TalesRunnerHK_News_DCWebHook 用來抓 [官網](www.talesrunner.com.hk)的遊戲公告, 整理資料之後丟到discord的webhook上面
>官方的鏈接是 www.talesrunner.com.hk
# 開始使用
## 環境需求
- Python 3.11.0 (https://www.python.org/)
- 被列在 requirements.txt 的配件清單
## 安裝方法
要使用 TalesRunnerHK_News_DCWebHook, 你需要安裝 python 以及使用 pip 去裝 requirements.txt 的前置資料
```
pip install -r requirements.txt
```
>requirements.txt
```
beautifulsoup4==4.11.2
discord_webhook==1.1.0
requests==2.28.2
```
## 修改配置
打開文件 "trmsg_page_parser.py", 在頂端可以找到 'webhook_links'
```py
webhook_links = []
```
把伺服器的 discord webhook 鏈接複製後丟到括號內, 像這樣:
```py
webhook_links = [ 'https://discordapp.com/api/webhooks/...']
```
如果你有多過一個鏈接, 可以用逗號隔開, 像這樣:
```py
webhook_links = [ 'https://discordapp.com/api/webhooks/...',
                  'https://discordapp.com/api/webhooks/...'
                ]
```
## 使用方式
打開你的黑窗口(cmd), 跑到檔案路徑下後, 輸入以下指令
```
py trmsg_page_parser.py
```

## 原理
從 trmsg_titles.txt 讀取緩存資料, 從下方三個網頁獲取 requests 
- 官網公告欄 'https://www.talesrunner.com.hk/news/MMXIII_news.html'
- 最新消息 'https://www.talesrunner.com.hk/notice/notice.php?type=system'
- 更新情報 'https://www.talesrunner.com.hk/notice/notice.php?type=patch'
>官網公告欄 的編碼是用 Big5, 最新情報 和 更新情報 是 UTF-8

用 Bs4 去抓 官網公告欄 的 "allNoticeContainer", 可以抓到
- 公告類別
- 公告鏈接
- 公告圖片

如果類別是 最新消息 或 更新情報, 就在其網頁找 td pointer, 抓前面的標籤(用previous)和後面的標籤(用next siblings以及抓上限值)

把整理好的訊息以discord webhook發佈.
