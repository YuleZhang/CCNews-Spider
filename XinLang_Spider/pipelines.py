# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
import csv
import os

class XinlangSpiderPipeline(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(os.path.dirname(__file__)) + '\\Dataset\\news_data.csv'
        #打开(创建)文件
        self.file = open(store_file, 'w',newline='')
        # csv写法
        self.writer = csv.writer(self.file)
        # 初始化表头
        print(['title'.encode('utf-8'), 'content'.encode(), 'url'.encode(), 'date'.encode(), 'source'.encode()])
        self.writer.writerow(['title', 'content', 'url', 'date', 'source'])

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        # self.filename = item['sonUrl'][7:-6].replace('/', '_') + '.txt'
        # self.file = open(item['subpath'] + '/' + self.filename, 'w')
        # self.file.write(item['sonUrl'] + '\n' + item['head'] + '\n' + item['time'] + '\n' + item['content'])
        self.writer.writerow([item['title'].encode("gbk", 'ignore').decode("gbk", "ignore"), item['content'].encode("gbk", 'ignore').decode("gbk", "ignore"), item['sonUrl'], item['time'], item['source'].encode("gbk", 'ignore').decode("gbk", "ignore")])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
