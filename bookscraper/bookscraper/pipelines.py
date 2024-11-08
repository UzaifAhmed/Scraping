# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2


class BookscraperPipeline:
    def process_item(self, item, spider):
        # adapter = ItemAdapter(item)

        # ## Strip all whitespaces from strings
        # field_names = adapter.field_names()
        # for field_name in field_names:
        #     if field_name != 'description' and field_name != 'price':
        #         value = adapter.get(field_name)
        #         adapter[field_name] = value[0].strip()

        # ## Category & Product Type --> switch to lowercase
        # lowercase_keys = ['category', 'product_type']
        # for lowercase_key in lowercase_keys:
        #     value = adapter.get(lowercase_key)
        #     adapter[lowercase_key] = value.lower()


        # ## Price --> convert to float and remove pound sign
        # price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        # for price_key in price_keys:
        #     value = adapter.get(price_key)
        #     value = value.replace('£', '')
        #     adapter[price_key] = float(value)
       

        # ## Availability --> extract number of books in stock
        # availability_string = adapter.get('availability')
        # split_string_array = availability_string.split('(')
        # if len(split_string_array) < 2:
        #     adapter['availability'] = 0
        # else:
        #     availability_array = split_string_array[1].split(' ')
        #     adapter['availability'] = int(availability_array[0])


        # ## Reviews --> convert string to number
        # num_reviews_string = adapter.get('num_reviews')
        # adapter['num_reviews'] = int(num_reviews_string)

        # ## Stars --> convert text to number
        # stars_string = adapter.get('stars')
        # split_stars_array = stars_string.split(' ')
        # stars_text_value = split_stars_array[1].lower()
        # if stars_text_value == "zero":
        #     adapter['stars'] = 0
        # elif stars_text_value == "one":
        #     adapter['stars'] = 1
        # elif stars_text_value == "two":
        #     adapter['stars'] = 2
        # elif stars_text_value == "three":
        #     adapter['stars'] = 3
        # elif stars_text_value == "four":
        #     adapter['stars'] = 4
        # elif stars_text_value == "five":
        #     adapter['stars'] = 5
        
        return item


class DuplicatePipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['url'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")

        else:
            self.names_seen.add(adapter['url'])
            return item


class SavingToPostgresqlPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = '12345678',
            database = 'book_scraping'
        )

        self.curr = self.conn.cursor()

    def store_db(self, item):
        self.curr.execute(""" insert into book_items values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item["name"],
            item["url"],
            item["image"],
            item["category"],
            item["currency"],
            item["price"],
            item["instock"],
            item["rating"],
            item["description"],
            item["upc"],
            item["num_of_reviews"],
            item["tax"]
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)

        return item