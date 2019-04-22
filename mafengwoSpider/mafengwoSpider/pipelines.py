# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from mafengwoSpider.items import MafengwospiderItem, SpotItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
def getinfo(item):
    if isinstance(item, MafengwospiderItem):
        sql = "INSERT INTO mdd(mdd_id, province, mdd_name, mdd_href)VALUES(%s, %s, %s, %s)"
        params = (item['mddid'], item['name'], item['cityname'], item['href'])
        return sql, params
    elif isinstance(item, SpotItem):
        sql = "INSERT INTO scenic_spots(mdd_id, mdd_name, spot_name, spot_href) VALUES (%s, %s, %s, %s)"
        params = (item['mddid'], item['cityname'], item['spotname'], item['spothref'])
        return sql, params
    else:
        sql = "INSERT INTO spot_comments(spot_name, comment_user, comment_text) VALUES (%s, %s, %s)"
        params = (str(item['spot_name']), item['comment_user'], item['comment_text'])
        return sql, params
class MafengwospiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode= True)
        self.cursor = self.connect.cursor();
    def process_item(self, item, spider):
        sql, params = getinfo(item)
        try:
            self.cursor.execute(sql, params)
            self.connect.commit()
        except Exception as e:
            # 事务回滚
            self.connect.rollback()
            print('except:', e.message)
 
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
