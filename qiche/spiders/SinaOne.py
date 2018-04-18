# -*- coding: utf-8 -*-
import scrapy
import re
from qiche.sinaItems import UrlItem

class SinaOneSpider(scrapy.Spider):
    name = 'SinaOne'
    allowed_domains = ['db.auto.sina.com.cn']
    start_urls = [
        'http://db.auto.sina.com.cn/list-1-0-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-2-0-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-3-0-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-4-0-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-5-0-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-6-0-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-0-5-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-0-7-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-0-11-0-0-0-0-0-0-9-0-1.html',
        'http://db.auto.sina.com.cn/list-0-15-0-0-0-0-0-0-9-0-1.html',
    ]

    def parse(self, response):
        #temp = [];
        Urls = UrlItem()
        pagina = response.css('.pagination')
        print pagina
        # 存在分页情况
        if pagina:
            # 获取一共有多少页
            total = pagina.xpath('script/text()').re_first(r'var totalPage=(\d)+;')
            total = int(total)
            i = 0;
            # 获取首页的url
            firstPage = 'http:' + pagina.xpath('a[@class="on"]/@href')[0].extract()
            firstPage = firstPage[::-1]
            while (i <= total):
                Urls['url'] = self.getUrl(firstPage, i)
                yield Urls
                i = i + 1;

        else:#不存在分页情况
            Urls['url'] = response.url
            yield Urls
            #temp.append(response.url)



        '''
        给定第一页的url和页数id，推出后续页面的url
        例如 第一页的url为：http://db.auto.sina.com.cn/list-1-0-0-0-0-0-0-0-9-0-1.html
        生成的后续页面url为:
        http://db.auto.sina.com.cn/list-1-0-0-0-0-0-0-0-9-0-(1+i).html
        '''
    def getUrl(self,url,i):
        matchObj = re.match(r'lmth\.(\d)?',url)
        return re.sub(r'lmth\.(\d)?','lmth.'+str(int(matchObj.group(1))+i),url)[::-1]




