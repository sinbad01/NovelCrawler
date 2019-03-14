# -*- coding: utf-8 -*-
# 从页面中解析出的xpath


def getDomain(idxs):
    return urls[idxs[0]][0]


def getXpathMap(idxs):
    return urls[idxs[0]][1]


def getBookInfo(idxs):
    return urls[idxs[0]][2][idxs[1]]


urls = [
# 0
    (
        ["www.miaobige.com"],

        {'title': '//*[@id="center"]/div[1]/h1/text()',
         'content': '//*[@id="content"]//p/text()',
         "next": '//*[@id="center"]/div[2]/a[5]//@href'},

        [
            # 第三卷 帝国之路 第111章 广南国的使者
            ('挽明', ['https://www.miaobige.com/read/13395/11940565.html'], 0),
            ('大明狂士', ['https://www.miaobige.com/read/12440/5801281.html'], 0),
        ],
    ),
# 1
    (
        ["www.sjtxt.com"],

        {'title': '//*[@id="info"]/div/h1/text()',
         'content': '//*[@id="content1"]/text()',
         "next": '//*[@id="info"]/div/div[2]/a[4]//@href'},

        [
            ('主神调查员 ', ['http://www.sjtxt.la/book/89809/20205503.html'], 190),
            ('大唐官 ', ['http://www.sjtxt.la/book/89699/19687098.html'], 0),
            ('带刀禁卫 ', ['http://www.sjtxt.la/book/90410/19808833.html'], 0),
            ('天国游戏 ', ['https://www.sjtxt.la/book/38211/3119606.html'], 0),
        ],
    ),
#2
    (
        ["www.x88dushu.com"],

        {'title': '/html/body/div[5]/h1/text()',
         'content': '/html/body/div[5]/div[4]/text()',
         "next": '//html/body/div[5]/div[1]/a[3]//@href'},

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
            ('被虫娘推倒', ['https://www.88dus.com/xiaoshuo/98/98336/33875260.html'], 0),
            ('华娱凶猛', ['https://www.x88dushu.com/xiaoshuo/109/109775/42782336.html'], 0),
            ('制霸好莱坞', ['https://www.x88dushu.com/xiaoshuo/63/63727/17132015.html'], 0),
        ],
    ),
# 3    
	(
        ["www.quanben.io"],

        {'title': '/html/body/div[3]/h1/text()',
         'content': '//*[@id="content"]/p/text()',
         "next": '/html/body/div[3]/div[3]/span[3]/a//@href'},

        [
            ('鸿隙', ['http://www.quanben.io/n/hongxi/1.html'], 0)
        ],
    ),


# 4
    (
        ["www.shumil.com"],

        {'title': '/html/head/title/text()',
         'content': '//div[@id="content"]/p[1]/text()',
         "next": '//div[@id="content"]/a[3]//@href'},

        [
            ('绿茵人生', ['http://www.shumil.com/lvyinrensheng/15520342.html'], 0),
            ('荣耀法兰西', ['http://www.shumil.com/rongyaofalanxi/16454984.html'], 0),
            ('华娱凶猛', ['http://www.shumil.com/huayuxiongmeng/21077139.html'], 0)
        ],
    ),
# 5
    (
        ["www.daomengren.com"],

        {'title': '//div[@class="bookname"]/h1/text()',
         'content': '//*[@id="content"]/p/text()',
         "next": '//div[@class="bottem1"]/a[4]//@href'},

        [
            ('娱乐春秋', ['http://www.daomengren.com/26_26400/13373898.html'], 0),
            ('仙官', ['http://www.daomengren.com/21_21005/8816244.html'], 0),
        ],
    ),
# 6
    # 2k中文
    (
        ["www.fpzw.com"],

        {'title': '//h2/text()',
         'content': '//p[@class="Text"]/text()',
         "next": '//div[@class="thumb"]/a[5]//@href'},
        [
            ('挽明', ['https://www.fpzw.com/xiaoshuo/108/108517/25243810.html'], 0)
        ],
    ),
# 7
    # 天眼看小说
    (
        ["novel.zhwenpg.com"],

        {'title': '//h2/text()',
         'content': '//table[5]//p',
         "next": '//table[4]/tr/td[3]/a/@href'},

        [
            ('战略级天使', ['https://novel.zhwenpg.com/r.php?id=402898'], 1)
        ],
    ),
    # 8
    # 有毒小说 需要
    (
        ["www.youdubook.com"],
        {'title': '//*[@id="ChapterMain"]/div[2]/text()',
         'content': '//*[@id="ChapterContent"]//p/text()',
         "next": '//*[@id="ChapterMain"]/div[6]/ul/li[3]/a/@href'},

        [
            ('旧日剑主', ['https://www.youdubook.com/readchapter/19486.html'], 0),
            ('灵吸怪备忘录', ['https://www.youdubook.com/book_detail/924.html'], 0)
        ],
    ),

   
# 9
    # 追书帮
    (

        ["www.zhuishubang.com"],
        {'title': '//h2/text()',
         'content': '//*[@class="articleCon"]/p/text()',
         "next": '//*[@class="page"]/a[3]/@href'},

        [
            ('大航海时代的德鲁伊', ['https://www.zhuishubang.com/24223/8698189.html'], 0),
            ('大航海时代的德鲁伊', ['https://www.zhuishubang.com/50754/18113338.html'], 0),
        ],
    ),

# 10
    # 花香居
    (

        ["www.huaxiangju.com"],
        {
        'title': '//h2/text()',
         'content': '//*[@class="articleCon"]/p/text()',
         "next": '//*[@class="page"]/a[3]/@href'},

        [
            ('邪恶组织注意事项', ['https://www.huaxiangju.com/2428/883581.html'], 0),
        ],
    ),
# 11
    # 有意思书院
    (

        ["www.heihei66.com"],
        {'title': '//p[@class="ctitle"]/text()',
         'content': '//div[@id="content"]/text()',
         "next": '//div[@class="bottomlink tc"]/a[7]/@href'},

        [
            ('我的大宝剑', ['https://www.heihei66.com/79/79542/28200871.html'], 0),
        ],
    ),
]
