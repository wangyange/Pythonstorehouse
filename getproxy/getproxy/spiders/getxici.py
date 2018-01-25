# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from getproxy.items import GetproxyItem


class GetxiciSpider(scrapy.Spider):
    name = 'getxici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/wn']

    def parse(self, response):
        data = response.xpath("//div[@class='clearfix proxies']/table[@id='ip_list']").extract()
        yield Request('http://www.xicidaili.com/wn',callback=self.GetDetail)


    def GetDetail(self,response):
        ipstress = response.xpath("//div[@class='clearfix proxies']/table[@id='ip_list']/tr/td[2]/text()").extract()
        port = response.xpath("//div[@class='clearfix proxies']/table[@id='ip_list']/tr/td[3]/text()").extract()
        area = response.xpath("//div[@class='clearfix proxies']/table[@id='ip_list']/tr/td[4]/a/text()").extract()
        ishide = response.xpath("//div[@class='clearfix proxies']/table[@id='ip_list']/tr/td[5]/text()").extract()
        print ipstress,port,area,ishide

        items = GetproxyItem()
        items['ipstress'] = ipstress
        items['port'] = port
        items['area'] = area
        items['ishide'] = ishide
        yield items