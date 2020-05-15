# -*- coding: utf-8 -*-
import sys

import scrapy
from scrapy import Request
from . import Rules
from . import AfterProcess
from .. import items





class NovelSpider(scrapy.Spider):
    name = 'novel'

    # site, book
    book_idx = Rules.IndexClass('www.wanbentxt.com', 8)
    allowed_domains = Rules.getDomain(book_idx)


    def __init__(self):
        super(NovelSpider, self).__init__()
        self.bookName = ''
        self.book_path = ''
        self.xpathMap = Rules.getXpathMap(self.book_idx)
        self.save = dict()

    def start_requests(self):
        if self.book_idx.book == -1:
            for book in Rules.getAllBookInfo(self.book_idx):
                self.bookName = book[0]
                self.book_path = r'E:\Download' + '\\' + self.bookName + ".txt"
                url = book[1]
                self.save[self.book_path] = url
                # print(self.bookName, url)
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            book = Rules.getBookInfo(self.book_idx)
            self.bookName = book[0]
            self.book_path = r'E:\Download' + '\\' + self.bookName + ".txt"
            url = book[1]
            self.save[self.book_path] = url
            # print(self.bookName, url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('parse ' + self.bookName)
        item = items.ChapterItem()

        x = [k for k, v in self.save.items() if v == response.url]
        path = x[0]

        selector = scrapy.Selector(response)
        item["next"] = selector.xpath(self.xpathMap['next']).extract_first()
        if item["next"] is None:
            self.logger.info("end of crawl")
            AfterProcess.regxProcess(path, self.book_idx.site)
            return

        self.logger.debug('next_href ' + item["next"])
        item["title"] = selector.xpath(self.xpathMap['title']).extract_first().strip()
        self.logger.info('title ' + item["title"])

        content = ''
        for para in selector.xpath(self.xpathMap['content']).extract():
            para = para.strip()
            self.logger.debug('para: ' + para)

            if len(para) > 0:
                content += para + "\n\n"
            self.logger.debug('para: ' + para)
            # print(str.encode(para))
        item["content"] = content

        # save chapter

        self.save_chapter(item, path)
        self.logger.debug('content: ' + content)

        next_href = response.urljoin(item["next"])
        self.logger.info('next_href: ' + next_href)
        self.logger.debug('response.url: ' + response.url)
        self.save[path] = next_href

        yield Request(next_href, callback=self.parse, dont_filter=True)
        # yield SplashRequest(next_href, callback=self.parse, endpoint='render.html', args=splash_args)

        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

    def save_chapter(self, item, path):
        with open(path, 'ab') as dest:
            title = '\n\n' + item["title"] + '\n\n\n'
            dest.write(title.encode(encoding="utf-8"))
            dest.write(item["content"].encode(encoding="utf-8"))

