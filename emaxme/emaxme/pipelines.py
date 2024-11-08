# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class EmaxmePipeline:
    def process_item(self, item, spider):
        return item
    
class SavingToPostgresPipeline(object):

    def __init__(self) -> None:
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = '12345678',
            database = 'emaxme_scraping'
        )

        self.curr = self.conn.cursor()

    def store_db(self, item):
        self.curr.execute(""" insert into mobile_data (item, image, url, color, screenSize, os, processor, ram, rom, currency, price, wasPrice, page_num, inStock) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item['name'],item['image'],item['url'],item['color'],item['screenSize'],item['os'],item['processor'],item['ram'],item['rom'],item['currency'],item['price'],item['wasPrice'],item['page_num'],item['inStock']
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)

        return item
