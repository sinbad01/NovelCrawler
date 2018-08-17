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
    ),


    (
        ["http://www.quanben.io"], {'title': '/html/body/div[3]/h1/text()',
                                     'content': '//*[@id="content"]/p/text()',
                                     'prev': '/html/body/div[3]/div[3]/span[1]/a//@href',
                                     "next": '/html/body/div[3]/div[3]/span[3]/a//@href'}
    ),

     (
        ["http://www.xinshuzx.cn"], {'title': '/html/body/div[4]/div/h2/text()',
                                     'content': '//div[@class="box_box"]//text()',
                                     'prev': '//a[@id="keyleft"]//@href',
                                     "next": '//a[@id="keyright"]//@href'}
    ),

    (
        ["http://www.shumil.com"], {'title': '/html/head/title/text()',
                                     'content': '//div[@id="content"]/p[1]/text()',
                                     'prev': '//div[@id="content"]/a[1]//@href',
                                     "next": '//div[@id="content"]/a[3]//@href'}
    ),

    (
        ["http://www.52dsm.com"], {'title': '//*[@id="center"]/div[1]/h1/text()',
                                     'content': '//*[@id="content"]/p/text()',
                                     'prev': '//*[@id="center"]/div[2]/a[1]//@href',
                                     "next": '//*[@id="center"]/div[2]/a[5]//@href'}
    ),
    (
        ["http://www.daomengren.com"], {'title': '//div[@class="bookname"]/h1/text()',
                                     'content': '//*[@id="content"]/p/text()',
                                     'prev': '//div[@class="bottem1"]/a[2]/@href',
                                     "next": '//div[@class="bottem1"]/a[4]//@href'}
    ),
]


bookInfo = [
    [
        # 第三卷 帝国之路 第111章 广南国的使者
        ('挽明', ['https://www.miaobige.com/read/13395/11940565.html'], 111),
    ],

    [
        ('主神调查员 ', ['http://www.sjtxt.la/book/89809/20205503.html'], 190),
        ('大唐官 ', ['http://www.sjtxt.la/book/89699/19687098.html'], 0),
        ('带刀禁卫 ', ['http://www.sjtxt.la/book/90410/19808833.html'], 0),
        ('天国游戏 ', ['https://www.sjtxt.la/book/38211/3119606.html'], 0),
    ],

    [
        ('娱乐春秋', ['https://www.88dushu.com/xiaoshuo/95/95205/34238897.html'], 301),
        ('难道我是神', ['http://www.88dushu.com/xiaoshuo/94/94425/34265065.html'], 336),
        ('大王饶命', ['http://www.88dushu.com/xiaoshuo/95/95143/31782995.html'], 0),
        ('打开你的任务日志', ['http://www.88dushu.com/xiaoshuo/96/96437/32467432.html'], 0),
        ('限制级末日症候', ['http://www.88dushu.com/xiaoshuo/19/19665/3629641.html'], 0),
        ('重生之地产大亨', ['https://www.88dushu.com/xiaoshuo/43/43027/11231347.html'], 0),
        ('重生之超级富豪', ['https://www.88dushu.com/xiaoshuo/88/88282/27281624.html'], 0),
        ('护花小神农', ['https://www.88dushu.com/xiaoshuo/80/80103/22558520.html'], 0),
        ('超级修理大师', ['https://www.88dushu.com/xiaoshuo/66/66961/18138426.html'], 0),
    ],

    [
        ('鸿隙', ['http://www.quanben.io/n/hongxi/1.html'], 0)
    ],

    [
        ('反正我是超能力者', ['http://www.xinshuzx.cn/fanzhengwoshichaonenlizhe/10982.html'], 1),
        ('我的大宝剑', ['http://www.xinshuzx.cn/wodedabaojian/10267.html'], 0)
    ],

    [
        ('绿茵人生', ['http://www.shumil.com/lvyinrensheng/15520342.html'], 0)
    ],

    [
        ('八一物流誉满全球', ['http://www.52dsm.com/chapter/10467/6045884.html'], 0)
    ],

    [
        ('娱乐春秋', ['http://www.daomengren.com/26_26400/13373898.html'], 0)
    ],
]

# site, book
idx = (7, 0)

# 保存路径
bookName = bookInfo[idx[0]][idx[1]][0]
xpathMap = siteInfo[idx[0]][1]

# 避免文件过大，拆分为多个文件
chapterCount = bookInfo[idx[0]][idx[1]][2]
chapterPerFile = 1000


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = siteInfo[idx[0]][0]
    start_urls = bookInfo[idx[0]][idx[1]][1]

    def __init__(self):
        super(NovelSpider, self).__init__()

        # 用于测试时及时停止
        self.count = chapterCount
        self.limit = chapterCount -1

        # self.cookies = self.transCookie('ctime=2018%2D01%2D13+05%3A41%3A20; click=A18505A; ASPSESSIONIDQAQCSCQT=PKMFHINDHMJHPJHHKMOHAACC; Hm_lvt_5d1243e3fcbf5e856c177a54c2ef34b3=1515750066; Hm_lpvt_5d1243e3fcbf5e856c177a54c2ef34b3=1515750096')

    def parse(self, response):
        logger.info('parse' + bookName)

        selector = scrapy.Selector(response)

        next_href = selector.xpath(xpathMap['next']).extract_first()
        if next_href is None:
            logger.info("end of crawl")
            return

        title = selector.xpath(xpathMap['title']).extract_first()
        content = ''
        for para in selector.xpath(xpathMap['content']).extract():
            para = para.strip()
            # logger.info('para: ' + para)

            if idx[0] == 4:
                if para.find('cgSize') != -1 or para.find("javascript") != -1:
                    continue
            if len(para) > 0:
                content += para + "\n\n"
            # logger.info('para: ' + para)
            # print(str.encode(para))

        # save chapter
        self.save_chapter('\n\n' + title + '\n' + next_href + '\n\n\n', content)
        logger.info('title: ' + title)
        # logger.info('content: ' + content)

        next_href = response.urljoin(next_href)
        logger.info('next_href: ' + next_href)
        # logger.info('response.url: ' + response.url)

        if self.count == self.limit:
            logger.info("exit")
            return
        self.count += 1

        # headers = {'Host': 'www.miaobige.com',
        #            'Connection': 'keep-alive',
        #            'Cache-Control': 'max-age=0',
        #            'Upgrade-Insecure-Requests': '1',
        #            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        #            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #            'DNT': '1',
        #            'Accept-Encoding': 'gzip, deflate, br',
        #            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        #            'Referer': response.url}

        yield Request(next_href, callback=self.parse, dont_filter=True)

        # 直接使用相对路径next_href即可，等同于 Request
        # yield response.follow(next_href, callback=self.parse)

    def save_chapter(self, title, content):
        bookPath = r'D:\Download' + '\\' + bookName + str(int(self.count / chapterPerFile)) + ".txt"
        with open(bookPath, 'ab') as dest:
            dest.write(title.encode(encoding="utf-8"))
            dest.write(content.encode(encoding="utf-8"))

    def transCookie(self, cookies):
        itemDict = {}
        items = cookies.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value

        print(itemDict)
        return itemDict
