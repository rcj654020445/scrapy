# -*- coding: utf-8 -*-
import scrapy
import codecs
import json
import re
import os
from qiche.items import TaobaoPrijian
from scrapy.http.request import Request


class TaobaosecondSpider(scrapy.Spider):
    name = 'TaobaoSecond'
    allowed_domains = ['https://s.taobao.com/']
    #start_urls = ['']

    def __init__(self):
        self.start_urls = [url for url in self.getUrls()]


    '''
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'cna': 'kdTTEatp2mACAXaQhSVEDwYB','otherx':'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0'
                                        ,'hng':'CN%7Czh-CN%7CCNY%7C156','enc':'JO5KIrVqnZ9zOloMEZQe3v%2BalbacpmuQoVVH7iCyrHCp3BV0iMXkT%2FjuFFInIN4aQXrtG%2BC918iRoXmkA32j7w%3D%3D',
                                        '_med':''})
    '''

    def url_decode(self, temp):
        while '\\' in temp:
            index = temp.find('\\')
            st = temp[index:index + 7]
            temp = temp.replace(st, '')

        index = temp.find('id')
        temp = temp[:index + 2] + '=' + temp[index + 2:]
        index = temp.find('ns')
        temp = temp[:index] + '&' + 'ns=' + temp[index + 2:]
        index = temp.find('abbucket')
        temp = 'https:' + temp[:index] + '&' + 'abbucket=' + temp[index + 8:]
        return temp

    def parse(self, response):
        url = response.url
        if r'list.tmall.com' in url:
            products = response.xpath('//div[@class="view grid-nosku"]/div[@class="product"]')
            for product in products:
                peijian  = TaobaoPrijian()
                peijian['imageSrc'] = product.xpath('./div[@class="product-iWrap"]/div[@class="productImg-wrap"]/a/img/@src')[0].extract()
                peijian['detailSrc'] = product.xpath('./div[@class="product-iWrap"]/div[@class="productImg-wrap"]/a/@href')[0].extract()
                peijian['price']  = product.xpath('./p[@class="productPrice"]/em/@title')[0].extract()
                peijian['title'] = product.xpath('./p[@class="productTitle"]/a/@title')[0].extract()
                #peijian['shop'] = product.xpath('./div[@class="productShop"]/a/text()')[0].extract()
                peijian['saleSize'] = product.xpath('./p[@class="productStatus"]/span')[0].xpath('em/text()')[0].extract()
                peijian['evalua'] = product.xpath('./p[@class="productStatus"]/span')[1].xpath('a/text()')[0].extract()
                yield peijian
        else:
            item = response.xpath('//script/text()').extract()
            pat = '"pic_url":"(.*?)","detail_url"(.*?),"view_price":"(.*?)","raw_title":"(.*?),"view_sales":"(.*?)","item_loc":"(.*?)"';
            urls = re.findall(pat, str(item))
            urls.pop(0)
            for url in urls:  # 解析url并放入数组中
                item = TaobaoPrijian()
                item['imageSrc'] = url[0]
                item['detailSrc'] = self.url_decode(temp=url[1])
                item['price'] = url[2]
                item['title'] = url[3]
                item['saleSize'] = url[4]
                item['evalua'] = url[5]
                yield item

    def getUrls(self):
        names = filter(lambda x: 'Taobao' in x and 'json' in x, os.listdir('D:/elaticserch/elaticserch/qiche/data'))
        if not names:
            print 'No Data File'
        filename = names[-1]
        f = codecs.open('D:/elaticserch/elaticserch/qiche/data/%s' % filename, 'r')
        for line in json.loads(f.read()):
            yield line['url']

