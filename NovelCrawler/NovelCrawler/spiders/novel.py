# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

# 从页面中解析出的xpath
xpathMap = {'title': '//*[@id="center"]/div[1]/h1/text()',
            'content': '//*[@id="content"]//p/text()',
            'prev': '//*[@id="center"]/div[2]/a[1]//@href',
            "next": '//*[@id="center"]/div[2]/a[5]//@href'}

# 最新章节 2017-12-30
# https://www.miaobige.com/read/13395/11394345.html
# title: 第三卷 帝国之路 第66章 陕西冒出的乱子

bookInfo = {'挽明': (['https://www.miaobige.com/read/13395/11394345.html'],
                   r'D:\Download\挽明.txt',
                   'https://www.miaobige.com/read/13395/'),
            '难道我是神': (['https://www.miaobige.com/read/18124/9706938.html'],
                      r'D:\Download\难道我是神.txt',
                      'https://www.miaobige.com/read/18124/'),
            '大王饶命': (['https://www.miaobige.com/read/18491/9930529.html'],
                      r'D:\Download\大王饶命.txt',
                      'https://www.miaobige.com/read/18491/')
            }
bookName = '大王饶命'


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.miaobige.com']
    start_urls = bookInfo[bookName][0]

    def __init__(self):
        super(NovelSpider, self).__init__()

        # 用于测试时及时停止
        self.count = 0
        # 保存路径
        self.path = bookInfo[bookName][1]

    def parse(self, response):
        selector = scrapy.Selector(response)

        # prev_href = selector.xpath(xpathMap['prev']).extract_first()
        # prev_href = 'https://www.miaobige.com/read/13395/' + prev_href
        # print('prev_href: ' + prev_href)

        next_href = selector.xpath(xpathMap['next']).extract_first()
        if next_href is None:
            print("end of crawl")
            return

        title = selector.xpath(xpathMap['title']).extract_first()
        content = ''
        for para in selector.xpath(xpathMap['content']).extract():
            content += para + "\n\n"

        # save chapter
        self.save_chapter('\n\n' + title + '\n\n\n', content)
        print('title: ' + title)
        # print('content: ' + content)

        next_href = bookInfo[bookName][2] + next_href
        print('next_href: ' + next_href)

        yield Request(next_href, callback=self.parse, dont_filter=True)

    def save_chapter(self, title, content):
        with open(self.path, 'ab') as dest:
            dest.write(title.encode(encoding="utf-8"))
            dest.write(content.encode(encoding="utf-8"))
