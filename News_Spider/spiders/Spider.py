# -*- coding: utf-8 -*-
import os
import sys
import json
import scrapy
from fake_useragent import UserAgent
sys.path.append(os.path.abspath('/News_Spider/News_Spider'))
from News_Spider.items import XinlangSpiderItem

ua = UserAgent()
# C114请求头
header_c114 = {
   'Accept': '*/*',
   'Accept-Language': 'en',
   "User-Agent":ua.random,
   'host': 'www.c114.com.cn',
   'Referer': 'http://www.c114.com.cn/tech/222.html',
   'X-Requested-With':'XMLHttpRequest'
}
# 飞象网请求头
header_cctime = {
    'Host':'www.cctime.com',
    'Referer':'http://www.cctime.com/list/5081.htm'
}
# 通信产业网请求头
header_ccidcom = {
    'Host':'www.ccidcom.com',
    'Origin':'http://www.ccidcom.com',
    'Referer':'http://www.ccidcom.com/yunying/index.html',
    'X-Requested-With':'XMLHttpRequest',
    'Cookie':'Hm_lvt_52fe61cd673e42ce80f6c570cf63b478=1584771439,1585283429,1585292109; ccidcom=a6uk4cb28mlttm0g1cdbq3maq6; HttpOnly; Hm_lpvt_52fe61cd673e42ce80f6c570cf63b478=1585292841'
}

# "http://www.ccidcom.com/getcolumnarts.do"
# 返回json格式数据ans=scrapy.FormRequest(url=url,formdata=my_data,headers=headers)
class newsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['sina.com.cn']
    urls = [
        'http://www.c114.com.cn/',
        'http://www.cctime.com/',
        'http://www.ccidcom.com/'
    ]
    max_pages = 15

    # 重写start_requests方法
    def start_requests(self):
        header = []
        header.append(header_c114)
        header.append(header_cctime)
        header.append(header_ccidcom)
        for i in range(len(self.urls)):
            yield scrapy.Request(url=self.urls[i], headers=header[i], callback=self.parse)

    def parse(self, response):
        # http://www.c114.com.cn/api/ajax/jishu.asp?p=2&idn=222&_=1584771742312
        item = XinlangSpiderItem()
        type_name = ['技术', '运营', '云计算']
        if response.url == self.urls[0]:
            item['website'] = response.url
            # 技术、运营、云计算
            # http://www.c114.com.cn/api/ajax/jishu.asp?p=2&idn=164,165,166,167,168,169,170,171,172,173,174,175&_=1585299764043
            type_news = ['jishu','aj_1812_1', 'aj_1805_2']
            type_idn = ['164,165,166,167,168,169,170,171,172,173,174,175','4049','117,118,119,4564,4329,4330,4331,4332']
            for i in range(len(type_name)):
                item['theme'] = type_name[i]
                parent_url = 'http://www.c114.com.cn/api/ajax/'+type_news[i]+'.asp?p={}&idn='+type_idn[i]
                # 查看新闻最多显示最近50页
                for page in range(2, self.max_pages):
                    new_url = parent_url.format(page)
                    print("cons url c114:" + str(parent_url).format(page))
                    yield scrapy.Request(url=new_url, headers=header_c114, meta={"item": item},callback=self.C114_parse,dont_filter=True)
        if response.url == self.urls[1]:
            item['website'] = response.url
            type_news = ['11108', '5081','12785']
            for i in range(len(type_name)):
                item['theme'] = type_name[i]
                parent_url = 'http://www.cctime.com/list/'+type_news[i]+'-{}.htm'
                # 查看新闻最多显示最近50页
                for page in range(1, self.max_pages):
                    new_url = parent_url.format(page)
                    print("cons url cctime:" + str(parent_url).format(page))
                    yield scrapy.Request(url=new_url, headers=header_cctime, meta={"item": item},callback=self.cctime_parse, dont_filter=True)
        if response.url == self.urls[2]:
            item['website'] = response.url
            post_data_1 = {
                'colnum_name': 'jishu',
                'start': '10',
                'page': '1',
                'csrf5e7da815ebd9d': 'c263645eb5f1f2a6ab3a918dd8380a39'
            }
            post_data_2 = {
                'colnum_name': 'yunying',
                'start': '10',
                'page': '1',
                'csrf5e7ddad122c02': '2ec89c4c2508bdfd8b21d12cd46be908'
            }
            post_data = []
            post_data.append(post_data_1)
            post_data.append(post_data_2)
            for i in range(len(type_name)-1):
                item['theme'] = type_name[i]
                parent_url = 'http://www.ccidcom.com/getcolumnarts.do'
                # 查看新闻最多显示最近30页
                for page in range(2, self.max_pages):
                    post_data[i]['page'] = str(page)
                    post_data[i]['start'] = str(page*10)
                    #scrapy.FormRequest(url=parent_url,formdata=post_data_1,headers=header_ccidcom)
                    yield scrapy.FormRequest(url=parent_url,formdata=post_data[i],headers=header_ccidcom,meta={"item": item},callback=self.ccidcom_parse, dont_filter=True)
    # C114页面解析
    # 注意页面是js动态返回的，不能通过xpath直接获得页面内容
    def C114_parse(self,response):
        # 解析url，放到队列
        item = response.meta['item']
        for ele in response.xpath("//div[@class='news']"):
            ele_url = ele.xpath("./a/@href").extract()[0]
            item['sonUrl'] = ele_url
            print(ele_url)
            yield scrapy.Request(ele_url, headers=header_c114, meta={"item": item},callback=self.C114_detail_parse,dont_filter=True)
    def C114_detail_parse(self,response):
        item = response.meta['item']
        print('开始解析文章:')
        # print("cnt2: %d"%cnt2)
        # item = XinlangSpiderItem()
        # url = item['sonUrl']
        # print(url)
        # item['sonUrl'] = url
        # 来源格式为'腾讯新闻 \xa0'，去除空格后的字符
        item['source'] = response.xpath("//div[@class='author']/text()").extract()[0].split(' ')[0]
        item['title'] = response.xpath("//div[@class='left-texts']/h1/text()").extract()[0]
        item['time'] = response.xpath("//div[@class='r_time']/text()").extract()[0]
        item['content'] = ''.join(response.xpath("//div[@class='text']/p/text()").extract())
        yield item

    # 飞象页面解析
    def cctime_parse(self,response):
        item = response.meta['item']
        for ele in response.xpath("//div[@class='kcs_list']"):
            ele_url = ele.xpath('./h2/a/@href').extract()[0]
            item['sonUrl'] = ele_url
            print(ele_url)
            yield scrapy.Request(ele_url, headers=header_cctime, meta={"item": item}, callback=self.cctime_detail_parse,dont_filter=True)
        pass
    def cctime_detail_parse(self,response):
        item = response.meta['item']
        title_tr = response.xpath("//tbody/tr")[0]
        time_tr = response.xpath("//tbody/tr")[3]
        item['title'] = title_tr.xpath("//h1/text()").extract()[0]
        item['time'] = time_tr.xpath("//tbody/tr/td")[0].xpath("//td[@class='dateAndSource']/text()").extract()[0].split('\xa0')[0]
        item['source'] = time_tr.xpath("//tbody/tr/td")[0].xpath("//td[@class='dateAndSource']/text()").extract()[0].split('\xa0')[2]
        item['content'] = ''.join(response.xpath("//div[@class='art_content']/p/text()").extract())
        yield item

    # 通信产业解析
    def ccidcom_parse(self,response):
        item = response.meta['item']
        json_cont = json.loads(response.text.encode('utf-8').decode('unicode-escape'),strict=False)
        for ele in json_cont['arts']:
            ele_url = self.urls[2] + ele['art_url']
            print("ele_url",ele_url)
            item['sonUrl'] = ele_url
            yield scrapy.Request(ele_url, headers=header_ccidcom, meta={"item": item}, callback=self.ccidcom_detail_parse,
                                 dont_filter=True)
    def ccidcom_detail_parse(self,response):
        item = response.meta['item']
        item['title'] = response.xpath("//div[@class='heading']/text()").extract()[0]
        item['time'] = response.xpath("//div[@class='pub']/span/text()").extract()[1]
        item['source'] = response.xpath("//div[@class='pub']/span/text()").extract()[0]
        item['content'] = "".join(response.xpath("//div[@class='content']/p/text()").extract())
        yield item