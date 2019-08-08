# -*- coding: utf-8 -*-
import scrapy
import re
from ppt_get.items import pptdownload_url


class PptSpider(scrapy.Spider):
    name = 'ppt'
    allowed_domains = ['ypppt.com']
    start_urls = ['http://www.ypppt.com/moban/']
    page_num = 0
    base_url = 'http://www.ypppt.com'

    def parse(self, response):
        self.page_num = response.xpath('//div[@class="page-navi"]/a[11]/@href').re_first('\d+')
        yield scrapy.Request(url='http://www.ypppt.com/moban/',callback=self.first_deep)
        for i in range(2,int(self.page_num)+1):
            yield scrapy.Request(url = 'http://www.ypppt.com/moban/list-{}.html'.format(i),callback=self.first_deep)
    
    def first_deep(self, response):
        url_list = response.xpath('//ul[@class="posts clear"]/li/a[2]/@href').extract()
        for i in url_list:
            yield scrapy.Request(url=self.base_url+i,callback=self.second_deep)
    
    def second_deep(self, response):
        url = response.xpath('//div[@class="button"]/a/@href').extract_first()
        yield scrapy.Request(url=self.base_url+url,callback=self.third_deep)
    
    def third_deep(self, response):
        item = pptdownload_url()
        download_url = response.xpath('//ul[@class="down clear"]/li/a/@href').extract()
        for i in range(len(download_url)):
            if 'http://' not in download_url[i]:
                download_url[i] = self.base_url + download_url[i]
        item['download_url'] = download_url
        title = response.xpath('//div[@class="de"]/h1/text()').extract_first().strip(' - 下载页')
        item['title'] = title
        yield item
