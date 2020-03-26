# -*- coding: utf-8 -*-
"""
经过长时间的分析发现，新浪微博的爬虫限制主要在host,需要经常换，下面是一些备用的host
'feed.mix.sina.com.cn','finance.sina.com.cn'
head = {"Sec-Fetch-Dest":"document","Sec-Fetch-Mode":"navigate","Upgrade-Insecure-Requests":"1","User-Agent":ua.random,"Connection":"keep-alive","host":"finance.sina.com.cn"}
"""
import os
import sys
import json
import scrapy
from fake_useragent import UserAgent
sys.path.append(os.path.abspath('C:/Users/Administrator/PycharmProjects/Scrapy_XinLang_Spider/XinLang_Spider/XinLang_Spider'))
from items import XinlangSpiderItem

ua = UserAgent()

header_getUrl = {
   'Accept': '*/*',
   'Accept-Language': 'en',
   "User-Agent":ua.random,
   'host': 'www.c114.com.cn',
   'Referer': 'http://www.c114.com.cn/tech/222.html',
   'X-Requested-With':'XMLHttpRequest'
}
header_getPage = {
   'Accept': '*/*',
   'Accept-Language': 'en',
   "User-Agent":ua.random,
   'host': 'news.sina.com.cn',
   'Referer': 'https://news.sina.com.cn/roll/',
   'Cookie': 'U_TRS1=00000086.a0a82148.5e060229.9d35c145; SINAGLOBAL=210.31.46.44_1577452075.397958; UM_distinctid=16f68d0c832a9-0da75971adbe38-6701b35-144000-16f68d0c8333c8; UOR=www.baidu.com,news.sina.com.cn,; __gads=ID=8143e64d8121f7ba:T=1580898085:S=ALNI_Majz_1aPz4TKM_XEgzM-8GqcrY2fA; lxlrttp=1578733570; SGUID=1584159577338_83803051; ArtiFSize=14; Apache=171.11.254.167_1584183260.370855; ULV=1584183343518:6:5:5:171.11.254.167_1584183260.370855:1584183259319; FEED-MIX-SINA-COM-CN=; U_TRS2=000000a7.b70579a0.5e6cdc4a.9853543b; rotatecount=3',
   'Sec-Fetch-Site': 'same-site'
}

cnt1 = 0
cnt2 = 0
class newsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://feed.mix.sina.com.cn/']

    def parse(self, response):
        # http://www.c114.com.cn/api/ajax/jishu.asp?p=2&idn=222&_=1584771742312
        type_news = ['164','165','166','168','169','170','171','172','173','174','222']
        for tp in type_news:
            parent_url = 'http://www.c114.com.cn/api/ajax/jishu.asp?p={}&idn='+tp+'&_={}'
            # 查看新闻最多显示最近50页
            for page in range(2,30):
                new_url = parent_url.format(page,1584771742310+page)
                print("new_url_my:"+ str(parent_url).format(page,1584771742310+page))
                yield scrapy.Request(url=new_url,headers=header_getUrl,callback=self.second_parse,dont_filter=True)

    # 注意页面是js动态返回的，不能通过xpath直接获得页面内容
    def second_parse(self,response):
        # 解析url，放到队列
        global cnt1
        cnt1+=1
        print("cnt1: %d"%cnt1)
        for ele in response.xpath("//div[@class='news']"):
            ele_url = ele.xpath("./a/@href").extract()[0]
            print(ele_url)
            yield scrapy.Request(ele_url, headers=header_getUrl, meta={"meta_2": ele_url},callback=self.detail_parse,dont_filter=True)

    def detail_parse(self,response):
        global cnt2
        cnt2 += 1
        print('开始解析文章:')
        print("cnt2: %d"%cnt2)
        item = XinlangSpiderItem()
        url = response.meta['meta_2']
        # print(url)
        item['sonUrl'] = url
        # 来源格式为'腾讯新闻 \xa0'，去除空格后的字符
        item['source'] = response.xpath("//div[@class='author']/text()").extract()[0].split(' ')[0]
        item['title'] = response.xpath("//div[@class='left-texts']/h1/text()").extract()[0]
        item['time'] = response.xpath("//div[@class='r_time']/text()").extract()[0]
        item['content'] = ''.join(response.xpath("//div[@class='text']/p/text()").extract())
        yield item

    # 查找s2第一次在s1中出现的位置
    # def index_of_str(self,s1, s2):
    #     lt = s1.split(s2, 1)
    #     if len(lt) == 1:
    #         return -1
    #     return len(lt[0])