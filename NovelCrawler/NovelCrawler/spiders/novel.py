# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

from . import SiteInfo
from NovelCrawler.items import ChapterItem

# # create logger with 'NovelSpider'
logger = logging.getLogger('NovelSpider')
logger.setLevel(logging.DEBUG)

# site, book
indexes = (-1, 0)

# 保存路径
bookName = SiteInfo.getBookInfo(indexes)[0]
xpathMap = SiteInfo.getXpathMap(indexes)

# 避免文件过大，拆分为多个文件
chapterCount = SiteInfo.getBookInfo(indexes)[2]
chapterPerFile = 1000


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = SiteInfo.getDomain(indexes)
    start_urls = SiteInfo.getBookInfo(indexes)[1]

    def __init__(self):
        super(NovelSpider, self).__init__()

        # 用于测试时，及时停止
        self.count = chapterCount
        self.limit = chapterCount - 1

    def parse(self, response):
        logger.info('parse ' + bookName)
        item = ChapterItem()

        selector = scrapy.Selector(response)

        item["next"] = selector.xpath(xpathMap['next']).extract_first()
        if item["next"] is None:
            logger.info("end of crawl")
            return
        # logger.info('next_href ' + item["next"])

        item["title"] = selector.xpath(xpathMap['title']).extract_first()
        # logger.info('title ' + item["next"])

        content = ''
        for para in selector.xpath(xpathMap['content']).extract():
            para = para.strip()
            # logger.info('para: ' + para)

            if len(para) > 0:
                content += para + "\n\n"
            # logger.info('para: ' + para)
            # print(str.encode(para))
        item["content"] = content

        # save chapter
        self.save_chapter(item)
        # logger.info('content: ' + content)

        next_href = response.urljoin(item["next"])
        logger.info('next_href: ' + next_href)
        # logger.info('response.url: ' + response.url)

        if self.count == self.limit:
            logger.info("exit")
            return
        self.count += 1

        yield Request(next_href, callback=self.parse, dont_filter=True)

        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

    def save_chapter(self, item):
        book_path = r'E:\Download' + '\\' + bookName + str(int(self.count / chapterPerFile)) + ".txt"
        title = '\n\n' + item["title"] + '\n' + item["next"] + '\n\n\n'
        with open(book_path, 'ab') as dest:
            dest.write(title.encode(encoding="utf-8"))
            dest.write(item["content"].encode(encoding="utf-8"))
