# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

# # create logger with 'NovelSpider'
logger = logging.getLogger('NovelSpider')
logger.setLevel(logging.DEBUG)

# 从页面中解析出的xpath
siteInfo = [
    (
        ["www.miaobige.com"], {'title': '//*[@id="center"]/div[1]/h1/text()',
                               'content': '//*[@id="content"]//p/text()',
                               'prev': '//*[@id="center"]/div[2]/a[1]//@href',
                               "next": '//*[@id="center"]/div[2]/a[5]//@href'}
    ),

    (
        ["www.sjtxt.com"], {'title': '//*[@id="info"]/div/h1/text()',
                            'content': '//*[@id="content1"]/text()',
                            'prev': '//*[@id="info"]/div/div[2]/a[2]//@href',
                            "next": '//*[@id="info"]/div/div[2]/a[4]//@href'}
    ),

    (
        ["http://www.88dushu.com"], {'title': '/html/body/div[5]/h1/text()',
                                     'content': '/html/body/div[5]/div[4]/text()',
                                     'prev': '/html/body/div[5]/div[1]/a[1]//@href',
                                     "next": '//html/body/div[5]/div[1]/a[3]//@href'}
    )
]

# 最新章节 2017-12-30
# https://www.miaobige.com/read/13395/11394345.html
# title: 第三卷 帝国之路 第66章 陕西冒出的乱子

bookInfo = [
    [
        # 第三卷 帝国之路 第74章 殿试选拔
        ('挽明', ['https://www.miaobige.com/read/13395/11502144.html']),
        # 320 雷霆万钧
        ('难道我是神', ['https://www.miaobige.com/read/18124/11502024.html']),
        #  451、李弦一拆台
        ('大王饶命', ['https://www.miaobige.com/read/18491/11492686.html']),
        ('娱乐春秋', ['https://www.miaobige.com/read/18505/9938701.html'])
    ],

    [
        # 第五十章 绝地武士
        ('主神调查员 ', ['http://www.sjtxt.com/book/89809/20212369.html'])
    ],

    [
        # 第五十章 绝地武士
        ('娱乐春秋', ['http://www.88dushu.com/xiaoshuo/95/95205/31816329.html'])
    ]
]
# site, book
idx = (0, 0)

# 保存路径
bookName = bookInfo[idx[0]][idx[1]][0]
bookPath = r'D:\Download' + '\\' + bookName + ".txt"
xpathMap = siteInfo[idx[0]][1]

class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = siteInfo[idx[0]][0]
    start_urls = bookInfo[idx[0]][idx[1]][1]

    def __init__(self):
        super(NovelSpider, self).__init__()

        # 用于测试时及时停止
        self.count = 0
        self.limit = -2
        self.cookies = self.transCookie('ctime=2018%2D01%2D13+05%3A41%3A20; click=A18505A; ASPSESSIONIDQAQCSCQT=PKMFHINDHMJHPJHHKMOHAACC; Hm_lvt_5d1243e3fcbf5e856c177a54c2ef34b3=1515750066; Hm_lpvt_5d1243e3fcbf5e856c177a54c2ef34b3=1515750096')

    def parse(self, response):
        logger.info('parse' + bookName)

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
            para = para.strip()
            if len(para) > 0:
                content += para + "\n\n"
            # logger.info('para: ' + para)
            # print(str.encode(para))

        # save chapter
        self.save_chapter('\n\n' + title + '\n\n\n', content)
        logger.info('title: ' + title)
        # logger.info('content: ' + content)

        next_href = response.urljoin(next_href)
        logger.info('next_href: ' + next_href)
        # logger.info('response.url: ' + response.url)

        if self.count == self.limit:
            logger.info("exit")
            return
        self.count += 1

        headers = {'Host': 'www.miaobige.com',
                   'Connection': 'keep-alive',
                   'Cache-Control': 'max-age=0',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'DNT': '1',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                   'Referer': response.url}
        # cookies = response.headers.getlist('Set-Cookie')
        # for c in cookies:
        #     print(c)
        yield Request(next_href, callback=self.parse, dont_filter=True, headers=headers)

        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

    def save_chapter(self, title, content):
        with open(bookPath, 'ab') as dest:
            dest.write(title.encode(encoding="utf-8"))
            dest.write(content.encode(encoding="utf-8"))

    def transCookie(self, cookies):
        a = ['ASPSESSIONIDQAQCSCQT', 'click', 'ctime']
        itemDict = {}
        items = cookies.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            # if key in a:
            itemDict[key] = value
        print(itemDict)
        return itemDict
