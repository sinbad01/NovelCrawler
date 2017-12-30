# -*- coding: utf-8 -*-
import scrapy


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.miaobige.com']
    start_urls = ['http://www.miaobige.com/']

    def parse(self, response):
        pass
