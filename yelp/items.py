# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    filename = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    categories = scrapy.Field()
    img = scrapy.Field()