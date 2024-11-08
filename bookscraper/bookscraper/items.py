# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookProducts(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    instock = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    num_of_reviews = scrapy.Field()
    tax = scrapy.Field()
