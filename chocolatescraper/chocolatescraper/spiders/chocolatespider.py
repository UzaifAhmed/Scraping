import scrapy
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemloaders import ChocolateProductLoader


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css('product-item')

        for product in products:

            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            # chocolate['name'] = product.css('a.product-item-meta__title::text').get()
            chocolate.add_css('name','a.product-item-meta__title::text')
            # chocolate['price'] = product.css('span.price').get().replace('<span class="price">\n        <span class="visually-hidden">Sale price</span>','').replace('</span>','')
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>') # (.*) for more then one replace
            # chocolate['url'] = product.css('div.product-item__image-wrapper a').attrib['href']
            chocolate.add_css('url', 'div.product-item__image-wrapper a::attr(href)')
            yield chocolate.load_item()

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(next_page_url, callback=self.parse)