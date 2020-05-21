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
    book_idx = Rules.IndexClass('www.wanbentxt.com', 0)
    allowed_domains = Rules.getDomain(book_idx)


    def __init__(self):
        super(NovelSpider, self).__init__()
        self.bookName = ''
        self.book_path = ''
        self.xpathMap = Rules.getXpathMap(self.book_idx)
        self.save = dict()
        self.path_format = r'E:\Download\{}.txt'

    def start_requests(self):
        if self.book_idx.book == -1:
            for book in Rules.getAllBookInfo(self.book_idx):
                self.bookName = book[0]
                url = book[1]
                self.save[self.bookName] = (0, [url, ''])
                # print(self.bookName, url)
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            book = Rules.getBookInfo(self.book_idx)
            self.bookName = book[0]
            url = book[1]
            self.save[self.bookName] = (0, [url, ''])
            # print(self.bookName, url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        x = [k for k, v in self.save.items() if v[1][v[0]] == response.url]
        book_name = x[0]
        path = self.path_format.format(book_name)

        self.logger.info('parse ' + book_name)
        item = items.ChapterItem()

        selector = scrapy.Selector(response)
        item["next"] = selector.xpath(self.xpathMap['next']).extract_first()
        if item["next"] is None:
            self.logger.info("end of crawl")
            self.save_last_url(book_name)
            AfterProcess.regxProcess(path, book_name, self.book_idx.site)
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

        idx, urls = self.save[book_name]
        idx = (idx + 1) % 2
        urls[idx] = next_href
        self.save[book_name] = (idx, urls)

        yield Request(next_href, callback=self.parse, dont_filter=True)
        # yield SplashRequest(next_href, callback=self.parse, endpoint='render.html', args=splash_args)

        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

    def save_chapter(self, item, path):
        with open(path, 'ab') as dest:
            title = '\n\n' + item["title"] + '\n\n\n'
            dest.write(title.encode(encoding="utf-8"))
            dest.write(item["content"].encode(encoding="utf-8"))

    def save_last_url(self, book_name):
        idx, urls = self.save[book_name]
        path = self.path_format.format('last_url')
        with open(path, 'ab') as dest:
            record = book_name + " " + urls[0] + " " + urls[1] + "\n"
            dest.write(record.encode(encoding="utf-8"))
