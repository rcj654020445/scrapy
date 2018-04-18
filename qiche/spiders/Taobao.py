# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from qiche.items import HrefItem

class TaobaoSpider(scrapy.Spider):
    name = 'Taobao'
    allowed_domains = ['https://car.tmall.com/']
    start_urls = ['https://car.tmall.com/']

    def parse(self, response):
        divs = response.xpath('//div[@class="category-box"]')[6:41]
        for div in divs:
            aas = div.xpath('./div[@class="box-cell-container"]/a[@class="box-cell"]')

            for a in aas:
                href = a.xpath('./@href')[0].extract()
                #判断是否是淘宝链接
                if r's.taobao.com' in href:
                    #默认10页数据
                    i = 1;
                    while i<11:
                        urls = HrefItem()
                        urls['url'] = 'https:'+href + '&s=' + str((i - 1) * 44)
                        i = i + 1;
                        yield urls



                #UrlItem = UrlItem()
                #UrlItem['url'] = a
                #print a
                #yield UrlItem


