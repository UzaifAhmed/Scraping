# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item


class PriceToUSDPipeline:
    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):

            #convreting price to float
            floatPrice = float(adapter['price'])

            #convertion
            adapter['price'] = floatPrice * self.gbpToUsdRate

            return item

        else:
            raise DropItem(f"Missing price in {item}")


class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")

        else:
            self.names_seen.add(adapter['name'])
            return item


class SavingToMysqlPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = '12345678',
            database = 'chocolate_scraping'
        )

        self.curr = self.conn.cursor()

    def store_db(self, item):
        self.curr.execute(""" insert into chocolate_items values (%s,%s,%s)""", (
            item["name"],
            item["price"],
            item["url"]
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)

        return item