# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PptGetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class pptdownload_url(scrapy.Item):
    title = scrapy.Field()
    download_url = scrapy.Field()
