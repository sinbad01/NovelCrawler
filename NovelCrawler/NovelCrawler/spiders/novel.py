# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

# # create logger with 'NovelSpider'
logger = logging.getLogger('NovelSpider')
logger.setLevel(logging.DEBUG)

# 从页面中解析出的xpath
xpathMap = {'title': '//*[@id="center"]/div[1]/h1/text()',
            'content': '//*[@id="content"]//p/text()',
            'prev': '//*[@id="center"]/div[2]/a[1]//@href',
            "next": '//*[@id="center"]/div[2]/a[5]//@href'}

# 最新章节 2017-12-30
# https://www.miaobige.com/read/13395/11394345.html
# title: 第三卷 帝国之路 第66章 陕西冒出的乱子

bookInfo = [
    # 第三卷 帝国之路 第74章 殿试选拔
    ('挽明', ['https://www.miaobige.com/read/13395/11502144.html']),
    # 320 雷霆万钧
    ('难道我是神', ['https://www.miaobige.com/read/18124/11502024.html']),
    #  451、李弦一拆台
    ('大王饶命', ['https://www.miaobige.com/read/18491/11492686.html'])
]
idx = 1
# 保存路径
bookPath = r'D:\Download' + '\\' + bookInfo[idx][0] + ".txt"


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.miaobige.com']
    start_urls = bookInfo[idx][1]

    def __init__(self):
        super(NovelSpider, self).__init__()

        # 用于测试时及时停止
        self.count = 0

    def parse(self, response):
        logger.info('parse')

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
            content += para + "\n\n"

        # save chapter
        self.save_chapter('\n\n' + title + '\n\n\n', content)
        logger.info('title: ' + title)

        next_href = response.urljoin(next_href)
        logger.info('next_href: ' + next_href)

        yield Request(next_href, callback=self.parse, dont_filter=True)

        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

    def save_chapter(self, title, content):
        with open(bookPath, 'ab') as dest:
            dest.write(title.encode(encoding="utf-8"))
            dest.write(content.encode(encoding="utf-8"))
