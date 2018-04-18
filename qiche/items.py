# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#href
class HrefItem(scrapy.Item):
    url = scrapy.Field()
    other_url = scrapy.Field()

class CheItem(scrapy.Item):
    pBrand = scrapy.Field()#一级品牌
    cBrand = scrapy.Field()#子品牌
    cMod = scrapy.Field()#车型
    cCBrand = scrapy.Field()#车款
    descMod = scrapy.Field()#车型详情描述
    year = scrapy.Field()#年份
    engine = scrapy.Field()#发动机型号
    cc = scrapy.Field()#排量
    power = scrapy.Field()#功率
    origin = scrapy.Field()#产地
    seat = scrapy.Field()#座位数

class PeiJian(scrapy.Item):
    name = scrapy.Field()
    shop = scrapy.Field()
    price = scrapy.Field()
    ads = scrapy.Field()

class TaobaoPrijian(scrapy.Item):
    imageSrc = scrapy.Field()
    detailSrc = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    #shop = scrapy.Field()
    saleSize = scrapy.Field()
    evalua  = scrapy.Field()

    
    









