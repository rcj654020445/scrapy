# -*- coding: utf-8 -*-
import scrapy
import os
import codecs
import re
import json
from qiche.items import PeiJian

class KupeistorageSpider(scrapy.Spider):
    name = 'kupeiStorage'
    allowed_domains = ['mall.kuparts.com']
    #start_urls = ['http://mall.kuparts.com/']

    def __init__(self):
        self.start_urls = [line for line in self.getUrls()]

    def parse(self, response):
        lis = response.xpath('//ul[@id="productlist"]/li[@class="item"]')
        for li in lis:
            peijian  = PeiJian()
            peijian['name'] = li.xpath('./div[@class="base"]/div[@class="t"]/a/@title')[0].extract()
            peijian['shop'] = li.xpath('./div[@class="base"]/div[@class="hidtit_2 com_name"]/a/@title')[0].extract()
            peijian['price'] = li.xpath('./div[@class="td td-3"]/span[@class="price"]/text()')[0].extract()
            peijian['ads'] = li.xpath('./div[@class="ads"]/text()')[0].extract()
            yield peijian
    def getUrls(self):
        file = filter(lambda x:'kupei' in x and 'json' in x,os.listdir('D:/elaticserch/elaticserch/qiche/data'))
        if not file:
            print 'No Data File'
        file = file[-1]
        f = codecs.open('D:/elaticserch/elaticserch/qiche/data/%s'%file,'r')
        for line in json.loads(f.read()):
            yield line['url']