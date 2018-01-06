# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

# # create logger with 'NovelSpider'
logger = logging.getLogger('NovelSpider')
logger.setLevel(logging.DEBUG)

# 从页面中解析出的xpath
xpathMap = {'title': '//*[@id="info"]/div/h1/text()',
            'content': '//*[@id="content1"]/text()',
            'prev': '//*[@id="info"]/div/div[2]/a[2]//@href',
            "next": '//*[@id="info"]/div/div[2]/a[4]//@href'}


bookInfo = [
    #  第五十章 绝地武士
    ('主神调查员 ', [' http://www.sjtxt.com/book/89809/20212369.html'])
]
idx = 0
# 保存路径
bookPath = r'D:\Download' + '\\' + bookInfo[idx][0] + ".txt"


class NovelSjtxtSpider(scrapy.Spider):
    name = 'novel_sjtxt'
    allowed_domains = ['www.sjtxt.com']
    start_urls = bookInfo[idx][1]

    def __init__(self):
        super(NovelSjtxtSpider, self).__init__()

        # 用于测试时及时停止
        self.count = 0
        self.limit = -1

    def parse(self, response):
        logger.info('parse NovelSjtxtSpider')

        selector = scrapy.Selector(response)

        # prev_href = selector.xpath(xpathMap['prev']).extract_first()
        # prev_href = 'https://www.miaobige.com/read/13395/' + prev_href
        # print('prev_href: ' + prev_href)

        next_href = selector.xpath(xpathMap['next']).extract_first()
        if next_href is None:
            logger.info("end of crawl")
            return

        title = selector.xpath(xpathMap['title']).extract_first()
        content = ''
        for para in selector.xpath(xpathMap['content']).extract():
            if para != '\n' and para != '\r':
                content += para + "\n\n"
            # logger.info('para: ' + para)
            # print(str.encode(para))

        # save chapter
        self.save_chapter('\n\n' + title + '\n\n\n', content)
        logger.info('title: ' + title)
        # logger.info('content: ' + content)

        next_href = response.urljoin(next_href)
        logger.info('next_href: ' + next_href)

        if self.count == self.limit:
            logger.info("exit")
            return
        self.count += 1

        yield Request(next_href, callback=self.parse, dont_filter=True)
        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

    def save_chapter(self, title, content):
        with open(bookPath, 'ab') as dest:
            dest.write(title.encode(encoding="utf-8"))
            dest.write(content.encode(encoding="utf-8"))
