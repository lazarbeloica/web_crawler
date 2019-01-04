# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ResponseData(scrapy.Item):
    '''
    Brief: Class holding the data to be sent to the spider pipeline
    '''
    response = scrapy.Field()


class ArtistData(scrapy.Item):
    '''
    Brief: Class holding the data to be sent to the spider pipeline
    '''
    artist_name = scrapy.Field()
    album_name = scrapy.Field()
    profile = scrapy.Field()
    track_list = scrapy.Field()
    album_version = scrapy.Field()
    album_rating = scrapy.Field()
    album_credits = scrapy.Field()
