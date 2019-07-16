# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class MovieHeavenBarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass

    movie_link = Field()
    movie_name = Field()
    movie_director = Field()
    movie_actors = Field()
    movie_publish_date = Field()
    movie_score = Field()
    movie_download_link = Field()
