# -*- coding: utf-8 -*-
import scrapy
import json
from qiche.items import HrefItem
import re

class OneSpider(scrapy.Spider):
    name = 'One'
    allowed_domains = ['data.auto.qq.com']
    start_urls = [
        'http://data.auto.qq.com/car_public/1/serial_style_1.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_2.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_3.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_4.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_5.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_6.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_7.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_8.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_9.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_9.shtml'
    ]

    def parse(self, response):
        for brand in response.css('.brand'):
            for group in brand.css('.group_b'):
                for right in group.css('.group_b_right'):
                    for div in right.css('.group_b_div_a'):
                        id = 'http://data.auto.qq.com/car_serial/'+div.xpath('a/@href').re_first(r'/car_serial/(\d+)/index\.shtml')+'/modelscompare.shtml'
                        hrefItem = HrefItem()
                        hrefItem['url'] = id
                        yield hrefItem


