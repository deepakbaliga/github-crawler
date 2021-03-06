# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubCrawlerProfileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    username = scrapy.Field()
    full_name = scrapy.Field()
    image_url = scrapy.Field()
    city  = scrapy.Field()
    joined_on  = scrapy.Field()
    email = scrapy.Field()
    bio = scrapy.Field()
    website = scrapy.Field()

    pass
