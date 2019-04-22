# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MafengwospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    cityname = scrapy.Field()
    mddid = scrapy.Field()
    href = scrapy.Field()
    page = scrapy.Field()
    pages = scrapy.Field()
class SpotItem(scrapy.Item):
    mddid = scrapy.Field()
    cityname = scrapy.Field()
    spotname = scrapy.Field()
    spothref = scrapy.Field()
class CommentItem(scrapy.Item):
    comment_user = scrapy.Field()
    comment_text = scrapy.Field()
    spot_name = scrapy.Field()
    spotid = scrapy.Field()
