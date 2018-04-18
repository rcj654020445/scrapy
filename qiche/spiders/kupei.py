# -*- coding: utf-8 -*-
import scrapy
from qiche.sinaItems import UrlItem

class KupeiSpider(scrapy.Spider):
    name = 'kupei'
    allowed_domains = ['mall.kuparts.com']
    start_urls = ['http://mall.kuparts.com/ProCategory/PartsIndex/']

    def parse(self, response):

        items = response.xpath('//div[@class="md"]/div[@class="item"]')

        for item in items:
            sub_items = item.xpath('./div[@class="sub_item"]')
            for sub_item in sub_items:
                spans = sub_item.xpath('./div[@class="sub_list clearfix"]/span[@class="sub_list_item"]')
                for span in spans:
                    url = span.xpath('./a/@href')[0].extract()
                    if url:
                        yield scrapy.Request(url=url, callback=self.getUrls, dont_filter=True)


    def getUrls(self,response):

        isPage = response.xpath('//span[@class="operate"]')
        #判断到底是否有分页
        if len(isPage) == 0:
            url = {};
            url['url'] = response.url
            return url
        else:
            urls = []
            #分析到底有多少页面
            pages = int(isPage.xpath('./select/option/@value')[-1].extract())
            i = 1;
            while (i < pages+1):
                url = {};
                url['url'] = response.url + '/' + str(i)
                urls.append(url)
                i = i + 1;
            return urls





