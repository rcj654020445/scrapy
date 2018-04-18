# -*- coding: utf-8 -*-
import scrapy
import codecs
import json
from qiche.sinaItems import UrlItem
import re
import os

class SinasecondSpider(scrapy.Spider):
    name = 'SinaSecond'
    allowed_domains = ['db.auto.sina.com.cn']

    def __init__(self):
        self.start_urls = [url for url in self.getUrls()]


    def parse(self, response):
        url = UrlItem()
        lis = response.xpath('//ul[@class ="like235 clearfix"]/li')
        for li in lis:
            line  = li.xpath('p[@class="title"]/a/@href')[0].extract()
            url['url']  = re.match(r'\/\/(.*)\/(\d+)?\/',line).group(2)
            yield url


    def getUrls(self):
        names = filter(lambda x: 'SinaOne' in x and 'json' in x, os.listdir('D:/elaticserch/elaticserch/qiche/data'))
        if not names:
            print 'No Data File'
        filename = names[-1]
        f = codecs.open('D:/elaticserch/elaticserch/qiche/data/%s' % filename, 'r')
        for line in json.loads(f.read()):
            yield line['url']

