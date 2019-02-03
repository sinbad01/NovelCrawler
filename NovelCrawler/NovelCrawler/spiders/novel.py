# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest

from . import Rules
from NovelCrawler.items import ChapterItem

# site, book
indexes = (-3, 0)

# 保存路径
bookName = Rules.getBookInfo(indexes)[0]
xpathMap = Rules.getXpathMap(indexes)

# 避免文件过大，拆分为多个文件
chapterCount = Rules.getBookInfo(indexes)[2]
chapterPerFile = 1000

splash_args = { 'wait': 1.5, }

class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = Rules.getDomain(indexes)
    start_urls = Rules.getBookInfo(indexes)[1]

    def __init__(self):
        super(NovelSpider, self).__init__()
        # 用于测试时，及时停止
        self.count = chapterCount
        self.limit = chapterCount - 1

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url, self.parse, endpoint='render.html', args=splash_args)

    def parse(self, response):
        self.logger.info('parse ' + bookName)
        item = ChapterItem()

        selector = scrapy.Selector(response)

        item["next"] = selector.xpath(xpathMap['next']).extract_first()
        if item["next"] is None:
            self.logger.info("end of crawl")
            return
        self.logger.debug('next_href ' + item["next"])

        item["title"] = selector.xpath(xpathMap['title']).extract_first()
        self.logger.debug('title ' + item["next"])

        content = ''
        for para in selector.xpath(xpathMap['content']).extract():
            para = para.strip()
            # self.logger.debug('para: ' + para)

            if len(para) > 0:
                content += para + "\n\n"
            # self.logger.debug('para: ' + para)
            # print(str.encode(para))
        item["content"] = content

        # save chapter
        self.save_chapter(item)
        self.logger.debug('content: ' + content)

        next_href = response.urljoin(item["next"])
        self.logger.info('next_href: ' + next_href)
        self.logger.debug('response.url: ' + response.url)

        if self.count == self.limit:
            self.logger.info("exit")
            return
        self.count += 1

        yield Request(next_href, callback=self.parse, dont_filter=True)
        # yield SplashRequest(next_href, callback=self.parse, endpoint='render.html', args=splash_args)

        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

    def save_chapter(self, item):
        book_path = r'E:\Download' + '\\' + bookName + str(int(self.count / chapterPerFile)) + ".txt"
        title = '\n\n' + item["title"] + '\n' + item["next"] + '\n\n\n'
        with open(book_path, 'ab') as dest:
            dest.write(title.encode(encoding="utf-8"))
            dest.write(item["content"].encode(encoding="utf-8"))
