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
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   "User-Agent":ua.random,
   'host': 'feed.mix.sina.com.cn',
   'Referer': 'https://news.sina.com.cn/roll/',
   'Cookie': 'U_TRS1=00000086.a0a82148.5e060229.9d35c145; SINAGLOBAL=210.31.46.44_1577452075.397958; UM_distinctid=16f68d0c832a9-0da75971adbe38-6701b35-144000-16f68d0c8333c8; UOR=www.baidu.com,news.sina.com.cn,; __gads=ID=8143e64d8121f7ba:T=1580898085:S=ALNI_Majz_1aPz4TKM_XEgzM-8GqcrY2fA; lxlrttp=1578733570; SGUID=1584159577338_83803051; ArtiFSize=14; Apache=171.11.254.167_1584183260.370855; ULV=1584183343518:6:5:5:171.11.254.167_1584183260.370855:1584183259319; FEED-MIX-SINA-COM-CN=; U_TRS2=000000a7.b70579a0.5e6cdc4a.9853543b; rotatecount=3',
   'Sec-Fetch-Site': 'same-site'
}
header_getPage = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   "User-Agent":ua.random,
   'host': 'news.sina.com.cn',
   'Referer': 'https://news.sina.com.cn/roll/',
   'Cookie': 'U_TRS1=00000086.a0a82148.5e060229.9d35c145; SINAGLOBAL=210.31.46.44_1577452075.397958; UM_distinctid=16f68d0c832a9-0da75971adbe38-6701b35-144000-16f68d0c8333c8; UOR=www.baidu.com,news.sina.com.cn,; __gads=ID=8143e64d8121f7ba:T=1580898085:S=ALNI_Majz_1aPz4TKM_XEgzM-8GqcrY2fA; lxlrttp=1578733570; SGUID=1584159577338_83803051; ArtiFSize=14; Apache=171.11.254.167_1584183260.370855; ULV=1584183343518:6:5:5:171.11.254.167_1584183260.370855:1584183259319; FEED-MIX-SINA-COM-CN=; U_TRS2=000000a7.b70579a0.5e6cdc4a.9853543b; rotatecount=3',
   'Sec-Fetch-Site': 'same-site'
}


class newsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1']

    def parse(self, response):
        parent_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page={}'
        ua = UserAgent()
        # 查看新闻最多显示最近50页
        for page in range(1,51):
            print("new_url_my:"+ str(parent_url).format(page))
            yield scrapy.Request(url=parent_url.format(page),headers=header_getUrl,callback=self.second_parse)

    # 注意页面是js动态返回的，不能通过xpath直接获得页面内容
    def second_parse(self,response):
        # 解析url，放到队列
        json_data = json.loads(response.text)
        for each in json_data['result']['data']:
            # https://finance.sina.com.cn/roll/2020-03-13/doc-iimxyqwa0214069.shtml
            # 请求头的host必须是Url首部的缩写否则就会404
            print("打印并访问文章url")
            sub = "sina"
            each_url = each['url']
            host_sta = each_url.find('//')
            host_end = self.index_of_str(each_url,sub)
            real_host = each_url[host_sta+2:host_end-1]
            header_getPage['host'] = real_host+".sina.com.cn"
            print(each['url'])
            #yield scrapy.Request(each_url, headers=settings.DEFAULT_REQUEST_HEADERS, meta={'meta_2': each_url},callback=self.detail_parse)
            yield scrapy.Request(each_url, headers=header_getPage,meta={"meta_2": each_url},callback=self.detail_parse)

    def detail_parse(self,response):
        print('开始解析文章:')
        item = XinlangSpiderItem()
        url = response.meta['meta_2']
        # print(url)
        item['sonUrl'] = url
        # xpath解析分别获得title、date以及source
        backup_title1 = response.xpath("//h1[@class='main-title']/text()").extract()
        backup_title2 = response.xpath("//h1[@id='artibodyTitle']/text()").extract()
        if len(backup_title1):
            item['title'] = backup_title1[0]
        elif len(backup_title2):
            item['title'] = backup_title2[0]
        else:
            item['title'] = ''
        item['time'] = response.xpath("//span[@class='date']/text()").extract()[0]
        # 通过页面解析发现文章来源有多种不同的class样式
        backup_Source1 = response.xpath("//span[@class='source']/text()").extract()
        backup_Source2 = response.xpath("//span[@class='source ent-source']/text()").extract()
        backup_Source3 = response.xpath("//a[@data-sudaclick='content_media_p']/text()").extract()
        if len(backup_Source1):
            item['source'] = backup_Source1[0]
        elif len(backup_Source2):
            item['source'] = backup_Source2[0]
        elif len(backup_Source3):
            item['source'] = backup_Source3[0]
        else:
            item['source'] = '暂无来源'
        # 新闻内容在不同的passage中，因此先合并再赋值给content
        item['content'] = ''.join(response.xpath("//div[@class='article']/p/text()").extract())
        print('start to save item')
        yield item
        #scrapy crawl news

    # 查找s2第一次在s1中出现的位置
    def index_of_str(self,s1, s2):
        lt = s1.split(s2, 1)
        if len(lt) == 1:
            return -1
        return len(lt[0])