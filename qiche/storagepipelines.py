# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch
import math


class StoragePipeline(object):
    def __init__(self, uri, index, type):
        self.uri = uri
        self.index = index
        self.type = type
        self.elaticserch = Elasticsearch(self.uri)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('URI'),
            index=crawler.settings.get('INDEX'),
            type =crawler.settings.get('TYPE')
        )


    def process_item(self, item, spider):
        body = {}

        body['pBrand'] = item['pBrand']
        body['cBrand'] = item['cBrand']
        body['cMod'] = item['cMod']
        body['cCBrand'] = item['cCBrand']
        body['descMod'] = item['descMod']
        body['year'] = item['year']
        body['engine'] = item['engine']
        if item['cc'].isdigit():
            body['cc'] = round(int(item['cc'])/100)/10
        body['power'] = item['power']
        body['origin'] = item['origin']
        #body['seat'] = item['seat']
        self.elaticserch.index(self.index,self.type,body)
        return item
