# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaNewhouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    total_sales = scrapy.Field()
    area_sales = scrapy.Field()
    area_name = scrapy.Field()
    xiaoqu_name = scrapy.Field()
    xiaoqu_price = scrapy.Field()
    price_danwei = scrapy.Field()
    xiaoqu_address = scrapy.Field()
    page_url = scrapy.Field()
    detail_url = scrapy.Field()
