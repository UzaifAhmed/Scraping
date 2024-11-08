# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EmaxmeItems(scrapy.Item):
    # define the fields for your item here like:
    color = scrapy.Field()
    os = scrapy.Field()
    screenSize = scrapy.Field()
    image = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    wasPrice = scrapy.Field()
    inStock = scrapy.Field()
    name = scrapy.Field()
    ram = scrapy.Field()
    rom = scrapy.Field()
    url = scrapy.Field()
    processor = scrapy.Field()
    page_num = scrapy.Field()
