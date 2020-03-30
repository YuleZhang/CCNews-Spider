# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XinlangSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 大类链接和url,如新闻　体育等
    title = scrapy.Field()
    # 小类链接和url，如新闻下面的国内　社会等
    # subUrl = scrapy.Field()
    # subTitle = scrapy.Field()
    # # 小类存储路径
    # subpath = scrapy.Field()

    # 子链接
    sonUrl = scrapy.Field()
    # 子链接里面的标题和内容 time
    head = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    theme = scrapy.Field()
    website = scrapy.Field()
    pass
