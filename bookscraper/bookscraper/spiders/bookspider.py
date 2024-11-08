import scrapy
from ..items import BookProducts


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

        #Books of the page
        products = response.css('article.product_pod div.image_container a::attr(href)').getall()

        for product in products:
            bk_url = self.start_urls[0]+'/'+product if 'catalogue/' in product else self.start_urls[0] +'/catalogue/'+product

            yield scrapy.Request(url=bk_url, callback=self.parse_book)

        # finding next page button
        try:
            next_page = response.css('li.next a').attrib['href']
            next_page = next_page.split('/')[-1] if '/' in next_page else next_page
        
        except:
            next_page = None
        
        if next_page is not None:
            next_page_url = 'https://books.toscrape.com/catalogue/' + next_page if 'catalogue' not in next_page else 'https://books.toscrape.com/' + next_page

            yield scrapy.Request(next_page_url, callback=self.parse)



    def parse_book(self, response):

        product_item = BookProducts()

        product_item['name'] = response.css('div.col-sm-6 h1::text').get()
        product_item['url'] = response.url      #   str(response).split(" ")[1][:-1]
        product_item['image'] = self.start_urls[0] + response.css('div.carousel-inner img::attr(src)').get()[5:]
        product_item['category'] = response.css('ul.breadcrumb li a::text').getall()[2]
        product_item['currency'] = '£'
        product_item['price'] = float(response.css('article.product_page td::text').getall()[2].split('£')[1])
        product_item['instock'] = response.css('article.product_page td::text').getall()[5]
        product_item['rating'] = response.css('div.row p')[2].xpath("@class").get().split(' ')[1]
        product_item['description'] = response.css('article.product_page p::text').getall()[10]
        product_item['upc'] = response.css('article.product_page td::text').getall()[0]
        product_item['num_of_reviews'] = int(response.css('article.product_page td::text').getall()[6])
        product_item['tax'] = float(response.css('article.product_page td::text').getall()[4].split('£')[1])
        
        yield product_item
