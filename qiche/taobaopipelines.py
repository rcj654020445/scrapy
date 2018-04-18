# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch
import math


class TaoBaoPipeline(object):
    def __init__(self, uri, index, type):
        self.uri = uri
        self.index = index
        self.type = type
        if self.elaticserch is None:
            self.elaticserch = Elasticsearch(self.uri)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('URI'),
            index=crawler.settings.get('TAOBAO_INDEX'),
            type =crawler.settings.get('TABOBAO_TYPE')
        )


    def process_item(self, item, spider):
        body = {}
        body['imageSrc'] = item['imageSrc']
        body['detailSrc'] = item['detailSrc']
        body['price'] = item['price']
        body['title'] = item['title']
        body['saleSize'] = item['saleSize']
        body['evalua'] = item['evalua']
        self.elaticserch.index(self.index,self.type,body)
        return item
