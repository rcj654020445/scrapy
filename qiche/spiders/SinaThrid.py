# -*- coding: utf-8 -*-
import scrapy
import codecs
import json
import re
import time
import os

class SinaThridSpider(scrapy.Spider):
    name = 'SinaThrid'
    allowed_domains = ['db.auto.sina.com.cn']

    def __init__(self):
        self.start_urls = [id for id in self.getIds()]


    def start_requests(self):
        for id in self.start_urls:
            t = time.time()
            url = 'http://db.auto.sina.com.cn/api/car/getFilterCar.json?subid='+id+'&niankuan=&derailleur_type=&product_status=1&outgas=&auto_type=&_='+str(int(round(t * 1000)))
            yield scrapy.Request(url=url,callback=self.pasrJson)



    def pasrJson(self,response):
        jsonBody = json.loads(response.body)
        items = [];
        for line in jsonBody:
            origin = u'国产';
            if  u'进口' in line['group_name']:
                origin = u'进口'
            item = {
                'pBrand':line['brand_name'],
                'cBrand':line['group_name'],
                'cMod':line['subbrand_name'],
                'cCBrand':line['cname'],
                'descMod':line['cname'],
                'year':re.match(r'(\d+)?',line['cname']).group(1),
                'engine':line['type'],
                'cc':str(line['outgas']),
                'power':line['max_power'],
                'origin':origin,
                #'seat':line['brand_name']
            }
            items.append(item)
        return items

    def getIds(self):
        names = filter(lambda x: 'SinaSecond' in x and 'json' in x, os.listdir('D:/elaticserch/elaticserch/qiche/data'))
        if not names:
            print 'No Data File'
        filename = names[-1]
        f = codecs.open('D:/elaticserch/elaticserch/qiche/data/%s' % filename, 'r')
        for line in json.loads(f.read()):
            yield line['url']

