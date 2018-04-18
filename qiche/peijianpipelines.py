# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch
import math


class PeiJianPipeline(object):
    def __init__(self, uri, index, type):
        self.uri = uri
        self.index = index
        self.type = type
        self.elaticserch = Elasticsearch(self.uri)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('URI'),
            index=crawler.settings.get('PEIJIAN_INDEX'),
            type =crawler.settings.get('PEIJIAN_TYPE')
        )


    def process_item(self, item, spider):
        body = {}
        body['name'] = item['name']
        body['shop'] = item['shop']
        body['price'] = item['price']
        body['ads'] = item['ads']
        self.elaticserch.index(self.index,self.type,body)
        return item
