# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NovelcrawlerPipeline(object):
    def process_item(self, item, spider):
        with open(item.get('path'), 'ab') as dest:
            dest.write(item.get('title').encode(encoding="utf-8"))
            dest.write(item.get('content').encode(encoding="utf-8"))
        return item
