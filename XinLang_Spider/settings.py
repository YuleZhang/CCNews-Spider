# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
# Scrapy settings for XinLang_Spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
ua=UserAgent()
BOT_NAME = 'XinLang_Spider'

SPIDER_MODULES = ['XinLang_Spider.spiders']
NEWSPIDER_MODULE = 'XinLang_Spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ua.random

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   "User-Agent":ua.random,
   'host': 'feed.mix.sina.com.cn',
   'Referer': 'https://news.sina.com.cn/roll/',
   'Cookie': 'U_TRS1=00000086.a0a82148.5e060229.9d35c145; SINAGLOBAL=210.31.46.44_1577452075.397958; UM_distinctid=16f68d0c832a9-0da75971adbe38-6701b35-144000-16f68d0c8333c8; UOR=www.baidu.com,news.sina.com.cn,; __gads=ID=8143e64d8121f7ba:T=1580898085:S=ALNI_Majz_1aPz4TKM_XEgzM-8GqcrY2fA; lxlrttp=1578733570; SGUID=1584159577338_83803051; ArtiFSize=14; Apache=171.11.254.167_1584183260.370855; ULV=1584183343518:6:5:5:171.11.254.167_1584183260.370855:1584183259319; FEED-MIX-SINA-COM-CN=; U_TRS2=000000a7.b70579a0.5e6cdc4a.9853543b; rotatecount=3',
   'Sec-Fetch-Site': 'same-site'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'XinLang_Spider.middlewares.XinlangSpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'XinLang_Spider.middlewares.XinlangSpiderDownloaderMiddleware': 543
}
RETRY_HTTP_CODES = [404, 403]
RETRY_TIMES = 3
# BACKUP_HEADERS_HOST = ['feed.mix.sina.com.cn','finance.sina.com.cn']
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 'XinLang_Spider.pipelines.XinlangSpiderPipeline': 250,
ITEM_PIPELINES = {

   'XinLang_Spider.pipelines.XinlangSpiderPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 30
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
