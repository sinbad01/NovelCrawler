# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     AfterProcess
   Description：   下载完毕后进行正则表达式替换，不同网站不同处理
   Author：       tongzhengyu
   date：          2019/12/16
-------------------------------------------------
"""
__author__ = 'tongzhengyu'

import re

def regxProcess(file, siteIdx):
    # if siteIdx != 19:
    #     return

    regxRules = {
        ".*anbentxt.*": "",
        ".*♂.*": "",
        "^.{0,4}(首发|最新|[完本神站文]).{0,4}?$": "",
        "</?[a-z]*>": "",
        "\(1/[1-9]\)$": "",
        ".*阅读站.*": "",
        "免费看精品好书请搜.": "",
        "-->>本章未完，点击下一页继续阅读": "",
        ".*浏览器.*": "",
        "^前往$": "",
    }

    content = ""
    with open(file, 'rb') as source:
        content = source.read().decode(encoding="utf-8")
        print(len(content))

        # 正则表达式替换
        # $ 在 flags=re.MULTILINE 时才起作用
        for pattern, repl in regxRules.items():
            content = re.sub(pattern, repl, content, flags=re.MULTILINE)

        # 匹配段落被拆分为2章的情况，
        p = '.\n*.*\([2-9]/[2-9]\)$\n*'
        end_punction = set('。！？“”')
        while True:
            match = re.search(p, content, flags=re.M)
            if match:
                # 判断最后一个字是否为标点符号
                last_word = content[match.start(0)]
                if last_word in end_punction:
                    # 以标点符号结尾，是2个段落，段落之间用"\n\n"连接
                    content = content[:match.start(0) + 1] + "\n\n" + content[match.end(0):]
                else:
                    # 连接被分割的连续文本
                    content = content[:match.start(0) + 1] + content[match.end(0):]
            else:
                break


    dest_file = file + ".mod"
    with open(dest_file, 'wb') as dest:
        dest.write(content.encode(encoding="utf-8"))



if __name__ == '__main__':
    file = r'E:\Download\蜘蛛巢城的魔人.txt'
    siteIdx = 0
    regxProcess(file, siteIdx)