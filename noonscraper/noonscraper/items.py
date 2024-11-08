# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PhoneProducts(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    currency = scrapy.Field()
    regular_price = scrapy.Field()
    offer_price = scrapy.Field()
    colour = scrapy.Field()
    ram = scrapy.Field()
    rom = scrapy.Field()
    os_version = scrapy.Field()
    processor = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()
    page_number = scrapy.Field()
