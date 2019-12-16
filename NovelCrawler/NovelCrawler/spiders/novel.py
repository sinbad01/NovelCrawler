# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
# from scrapy_splash import SplashRequest

from . import Rules
from . import AfterProcess
from NovelCrawler.items import ChapterItem

# site, book
indexes = (-1, 4)

# 保存路径
bookName = Rules.getBookInfo(indexes)[0]
book_path = r'E:\Download' + '\\' + bookName + ".txt"
xpathMap = Rules.getXpathMap(indexes)
# 避免文件过大，拆分为多个文件
chapterCount = Rules.getBookInfo(indexes)[2]

splash_args = {'wait': 1.5, }


def save_chapter(item):
    with open(book_path, 'ab') as dest:
        title = '\n\n' + item["title"] + '\n' + item["next"] + '\n\n\n'
        dest.write(title.encode(encoding="utf-8"))
        dest.write(item["content"].encode(encoding="utf-8"))


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = Rules.getDomain(indexes)
    start_urls = Rules.getBookInfo(indexes)[1]

    def __init__(self):
        super(NovelSpider, self).__init__()
        # 用于测试时，及时停止
        self.count = chapterCount
        self.limit = chapterCount - 1

    def parse(self, response):
        self.logger.info('parse ' + bookName)
        item = ChapterItem()

        selector = scrapy.Selector(response)

        item["next"] = selector.xpath(xpathMap['next']).extract_first()
        if item["next"] is None:
            self.logger.info("end of crawl")
            return

        self.logger.debug('next_href ' + item["next"])
        item["title"] = selector.xpath(xpathMap['title']).extract_first().strip()
        self.logger.info('title ' + item["title"])

        content = ''
        for para in selector.xpath(xpathMap['content']).extract():
            para = para.strip()
            self.logger.debug('para: ' + para)

            if len(para) > 0:
                content += para + "\n\n"
            self.logger.debug('para: ' + para)
            # print(str.encode(para))
        item["content"] = content

        # save chapter
        save_chapter(item)
        self.logger.debug('content: ' + content)

        next_href = response.urljoin(item["next"])
        self.logger.info('next_href: ' + next_href)
        self.logger.debug('response.url: ' + response.url)

        if self.count == self.limit:
            AfterProcess.regxProcess(book_path, indexes[0])
            self.logger.info("exit")
            return
        self.count += 1

        yield Request(next_href, callback=self.parse, dont_filter=True)
        # yield SplashRequest(next_href, callback=self.parse, endpoint='render.html', args=splash_args)

        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

