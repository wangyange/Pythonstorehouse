# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetproxyItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    ipstress = scrapy.Field()
    port = scrapy.Field()
    area = scrapy.Field()
    ishide = scrapy.Field()
