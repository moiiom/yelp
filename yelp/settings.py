BOT_NAME = 'yelp'

SPIDER_MODULES = ['yelp.spiders']
NEWSPIDER_MODULE = 'yelp.spiders'

ROBOTSTXT_OBEY = False
# DEPTH_LIMIT = 3

DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_TIMEOUT = 10

COOKIES_ENABLED = False

# Retry when proxies fail
RETRY_TIMES = 3

# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 80,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'yelp.middlewares.MyUserAgentMiddleware': 555,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'yelp.middlewares.MyHttpProxyMiddleware': 750,
    # 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    # 'yelp.HttpProxyMiddleware.HttpProxyMiddleware': 543,
}

ITEM_PIPELINES = {
    'yelp.pipelines.YelpPipeline': 300,
}


# 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
# DEFAULT_REQUEST_HEADERS = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, sdch',
#     'Accept-Language': 'en-us,en;q=0.8',
#     'Connection': 'keep-alive',
#     'Cookie': '__cfduid=df05dc588e6169fe925d8ebc536543c481469942076; yuv=r9QPlV9AEGDAYweiazb7asM-r0rkG2-0J8--0-IxAXN-DOQAOCxkcoqsj4PTKfU3qb1mzMhjqol3XO21SZMTBN9xr8fmz-Ta; fd=0; hl=en_US; qntcst=D; __qca=P0-724878990-1469942078641; D_SID=103.250.225.195:OZPnHYpeFF07BAyyIke1nIYEyzYNDQMvE5hmnIc0UN0; location=%7B%22city%22%3A+%22Aberdeen%22%2C+%22zip%22%3A+%22%22%2C+%22address1%22%3A+%22%22%2C+%22address2%22%3A+%22%22%2C+%22address3%22%3A+%22%22%2C+%22state%22%3A+%22WA%22%2C+%22country%22%3A+%22US%22%2C+%22unformatted%22%3A+%22Aberdeen%2C+WA%22%7D; bse=bf65531adaca1d2e72b690e6be5f74e0; __ar_v4=BHPKS4B4ONEJJMGH4QCJZR%3A20160730%3A21%7CQB5JPFIKRZDSBOZSULG4YB%3A20160730%3A21%7C7YX6SJQ4RZAMPB6LZ7CHFF%3A20160730%3A21; _ga=GA1.2.4BFFD3D1BC46BEC1; D_PID=1AEE13A2-C955-30B6-B8E3-3EF40A8E9B22; D_IID=9F637EDA-7165-3822-A5A3-3EBF65B92A42; D_UID=51FCC154-EED3-3ABA-A4D8-5D63B8A20D38; D_HID=ylixXELYKc40EvVkVj2r6Lw4x97BPBRjoSwBe7kARPI; D_ZID=1F30F2E4-83CE-3C82-B723-5D3A96438FF6',
#     'Host': 'www.yelp.com',
#     'Referer': 'http://www.yelp.com/search?find_loc=Birmingham&cflt=active',
#     'Upgrade-Insecure-Requests': 1,
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36'
# }

# custom setting

DATA_BASE_PATH = "/home/jason/scrapy_data"

# four hour
FETCH_PROXY_INTERVAL = 14400

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
