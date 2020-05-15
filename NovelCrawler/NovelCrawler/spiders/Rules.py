# -*- coding: utf-8 -*-
# 从页面中解析出的xpath

import collections

IndexClass = collections.namedtuple('IndexClass', ['site', 'book'])

def getDomain(idxs):
    return idxs.site

def getXpathMap(idxs):
    return urls[idxs.site][0]

def getBookInfo(idxs):
    return urls[idxs.site][1][idxs.book]

def getAllBookInfo(idxs):
    return urls[idxs.site][1]

urls = {
    # 天眼看小说
    "novel.zhwenpg.com":
        (
            {'title': '//h2/text()',
             'content': '//table[5]//p',
             "next": '//table[4]/tr/td[3]/a/@href'},

            [
                # 155
                ('战略级天使', 'https://novel.zhwenpg.com/r.php?id=462622', 1)
            ],
        ),

    # 有毒小说 需要
    "www.youdubook.com":
        (
            {'title': '//*[@id="ChapterMain"]/div[2]/text()',
             'content': '//*[@id="ChapterContent"]//p/text()',
             "next": '//*[@id="ChapterMain"]/div[6]/ul/li[3]/a/@href'},

            [
                ('旧日剑主', 'https://www.youdubook.com/readchapter/19486.html', 0),
                ('灵吸怪备忘录', 'https://www.youdubook.com/book_detail/924.html', 0)
            ],
        ),

    # 笔趣阁
    "www.bqg5200.com":
        (
            {'title': '//h1/text()',
             'content': '//div[@id="content"]/text()',
             "next": '//*[@id="container"]/div[4]/div[2]/a[5]/@href'},

            [
                ('我的知识能卖钱', 'https://www.bqg5200.com/xiaoshuo/35/35007/15232653.html', 0),
                ('走进修仙', 'https://www.bqg5200.com/xiaoshuo/3/3385/1922479.html', 0),
            ],
        ),

    # 完本神站，有乱码，疑似OCR
    "www.wanbentxt.com":
        (
            {'title': '//h2/text()',
             'content': '//div[@class="readerCon"]/p/text()',
             "next": '//div[@class="readPage"]/a[3]/@href'},

            [
                # 506
                ('火热的年代', 'https://www.wanbentxt.com/21849/18576939.html', 0),
                # 963
                ('旧日剑主', 'https://www.wanbentxt.com/19482/18576962.html', 0),
                # 60.朕又不是巴列奥略家的种
                ('你的帝国', 'https://www.wanbentxt.com/19486/17827528.html', 0),
                # 444
                ('蜘蛛巢城的魔人', 'https://www.wanbentxt.com/21851/18685192.html', 0),
                # 第九十七章 剑压城
                ('维止王朝的剑客信条', 'https://www.wanbentxt.com/21711/17784373.html', 0),
                ('绿龙筑巢记', 'https://www.wanbentxt.com/19484/14040188.html', 0),
                ('灵吸怪备忘录', 'https://www.wanbentxt.com/19485/14234523.html', 0),
                ('战略级天使', 'https://www.wanbentxt.com/15287/13761884.html', 0),

                ('变异的万法之书', 'https://www.wanbentxt.com/21856/13848186.html', 0),

                # ('[综武侠]圣僧', 'https://www.wanbentxt.com/93966676/17490381.html', 0),
                # ('大航海时代的德鲁伊', 'https://www.wanbentxt.com/21850/13846689.html', 0),
            ],
        ),

    # 掌阅 书山
    "shushan.zhangyue.net":
        (
            {'title': '//h2/text()',
             'content': '//div[@class="art_con"]/p/text()',
             "next": '//div[@class="art-box-right"]/ul/li[5]/a/@href'},
            [

                ('汉宫案', 'http://shushan.zhangyue.net/book/88333/13418439', 0),
                ('伏龙', 'http://shushan.zhangyue.net/book/88246/13412092', 0),
            ],
        ),
}


if __name__ == '__main__':
    book_idx = IndexClass('www.wanbentxt.com', 8)
    book = getBookInfo(book_idx)
    print(book)
    bookname = book[0]
    url = book[1]
    print(bookname, url)

