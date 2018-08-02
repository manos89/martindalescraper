# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MartindaleItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    people1 = scrapy.Field()
    people2 = scrapy.Field()
    people3 = scrapy.Field()
    first_name = scrapy.Field()
    year_established = scrapy.Field()
    size = scrapy.Field()
    practises = scrapy.Field()
    phone1 = scrapy.Field()
    phone2 = scrapy.Field()
    website = scrapy.Field()
    county = scrapy.Field()
    postal_code = scrapy.Field()
    town = scrapy.Field()
    stars = scrapy.Field()
    number_of_stars = scrapy.Field()
    recommendation_number = scrapy.Field()
    recommendation_percentage = scrapy.Field()
