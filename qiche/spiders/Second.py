# -*- coding: utf-8 -*-
import scrapy
import json
from qiche.items import CheItem
import os
import re
import codecs
from scrapy.contrib.loader import ItemLoader

class SecondSpider(scrapy.Spider):
    name = 'Second'
    allowed_domains = ['data.auto.qq.com']
    start_urls = [
    ]

    def __init__(self):
        self.start_urls = [url for url in self.getUrls()]

    def parse(self, response):
        if response.xpath('//div[@class="right"]/ul/li'):
            #属性栏的总html
            c1 = response.xpath('//div[@class="data cl"]/ul')
            # 车型个数
            j = 0
            for li in response.xpath('//div[@class="right"]/ul[@class="name blue1"]/li'):
                cheitem = CheItem()
                i = 0
                #初始化车型名称
                if len(li.xpath('a[@target="_blank"]/@title')):
                    title = li.xpath('a[@target="_blank"]/@title')[0].extract()
                else:
                    title = li.xpath('a[@target="_blank"]/text()')[0].extract()
                #一级品牌，子品牌，车型，车款，车型详情描述
                cheitem['pBrand'] = response.xpath('//div[@class="header-bread"]/a/text()')[2].extract()
                cheitem['cBrand'] = response.xpath('//div[@class="header-bread"]/a/text()')[3].extract()
                cheitem['cMod'] = response.xpath('//div[@class="trigger"]/a[@class="TName"]/text()')[0].extract()
                cheitem['cCBrand'] = title
                cheitem['descMod'] = response.xpath('//div[@class="trigger"]/a[@class="TName"]/text()')[0].extract()+' '+title
                temp = {}
                k = 0
                #属性栏数
                for node in response.xpath('//ul[@id="config_name"]/li'):
                    
                    #下面有a连接的
                    if len(node.xpath('./a/text()').extract()):
                        j = str(j)
                        max = len(c1.xpath('li[@id="car_' + j + '"]/ul/li')) - 1
                        if k <= max:
                            temp[node.xpath('./a/text()')[0].extract()] = c1.xpath('li[@id="car_'+j+'"]/ul/li')[k].xpath('./text()')[0].extract()
                        j = int(j)
                    #下面无a连接的
                    if len(node.xpath('./text()').extract()):
                        j = str(j)
                        max = len(c1.xpath('li[@id="car_' + j + '"]/ul/li')) - 1
                        if k <= max:
                            temp[node.xpath('./text()')[0].extract()] = c1.xpath('li[@id="car_'+j+'"]/ul/li')[k].xpath('./text()')[0].extract()
                        j = int(j)

                    #记录遍历到的属性栏位位置
                    k = k + 1
                    print j

                    if len(node.xpath('./h3/text()').extract()):
                        if i == 1:
                            cheitem['year'] = temp[u'年款']
                            cheitem['power'] = temp[u'最大功率(kW/rpm)']
                            cheitem['origin'] = temp[u'产地']
                        if i == 2:
                            cheitem['seat'] = temp[u'座位数(个)']
                        if i == 3:
                            cheitem['engine'] = temp[u'发动机']
                            cheitem['cc'] = temp[u'排气量(cc)']

                        '''
                        if i == 4:
                            cheitem['dipan'] = temp
                        if i == 5:
                            cheitem['xingneng'] = temp
                        if i == 6:
                            cheitem['anquan'] = temp
                        if i == 7:
                            cheitem['cheshen'] = temp
                        if i == 8:
                            cheitem['neibu'] = temp
                        if i == 9:
                            cheitem['zuoyi'] = temp
                        if i == 10:
                            cheitem['media'] = temp
                        if i == 11:
                            cheitem['light'] = temp
                        if i == 12:
                            cheitem['glass'] = temp
                        if i == 13:
                            cheitem['other'] = temp
                        '''
                        i += 1
                        temp = {}
                        #k = k + 1
                        continue
                j +=1
                
                yield cheitem








    def getUrls(self):
        names = filter(lambda x: 'One' in x and  'json' in x,os.listdir('D:/elaticserch/elaticserch/qiche/data'))
        if not names:
            print 'No Data File'
        filename =  names[-1]
        f = codecs.open('D:/elaticserch/elaticserch/qiche/data/%s' % filename, 'r')
        for line in json.loads(f.read()):
            yield line['url']