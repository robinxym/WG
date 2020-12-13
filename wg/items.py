# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

    user_name = scrapy.Field()
    comment_rating = scrapy.Field()
    # image_urls = scrapy.Field()
    # images = scrapy.Field()
    comment_date = scrapy.Field()
    comment_content = scrapy.Field()
