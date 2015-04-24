# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SeniorProfile(scrapy.Item):
    pass


class WhitepagesItem(scrapy.Item):
    name = scrapy.Field()
    major = scrapy.Field()
    email = scrapy.Field()
    college = scrapy.Field()
    class_year = scrapy.Field()
