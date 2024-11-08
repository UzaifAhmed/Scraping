import scrapy, json
from ..items import EmaxmeItems

def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v=''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v =''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie': continue
            if strip_cl and k.lower() == 'content-length': continue
            if k in strip_headers: continue
            d[k] = v
    return d

class EmaxmespiderSpider(scrapy.Spider):
    name = "emaxmeSpider"
    allowed_domains = ["uae.emaxme.com","3hwowx4270-dsn.algolia.net"]
    # start_urls = ["https://uae.emaxme.com/shop-mobile?p=1"]
    api_url = 'https://3hwowx4270-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.24.0)%3B%20Browser'
    go = 1

    h = get_headers('''
                    Accept: */*
                    Accept-Encoding: gzip, deflate, br, zstd
                    Accept-Language: en-US,en;q=0.9
                    Connection: keep-alive
                    Content-Length: 420
                    Host: 3hwowx4270-dsn.algolia.net
                    Origin: https://uae.emaxme.com
                    Sec-Fetch-Dest: empty
                    Sec-Fetch-Mode: cors
                    Sec-Fetch-Site: cross-site
                    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
                    content-type: application/x-www-form-urlencoded
                    sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
                    sec-ch-ua-mobile: ?0
                    sec-ch-ua-platform: "Windows"
                    x-algolia-api-key: 4c4f62629d66d4e9463ddb94b9217afb
                    x-algolia-application-id: 3HWOWX4270
                    ''')
    
    payload = '{"requests":[{"indexName":"prod_uae_emax_product","query":"*","params":"facets=*&page=1&hitsPerPage=48&attributesToRetrieve=*&attributesToHighlight=%5B%22name%22%5D&maxValuesPerFacet=1000&getRankingInfo=true&facetFilters=%5B%22inStock%3A1%22%2C%22approvalStatus%3A1%22%2C%5B%22allCategories%3Amobile%22%5D%5D&numericFilters=%5B%22price%20%3E%200%22%5D&clickAnalytics=true&analyticsTags=%5B%22en%22%2C%22Desktop%22%5D"}]}'

    def start_requests(self):
        print(self.api_url)
        yield scrapy.Request(url=self.api_url, headers=self.h, body=self.payload, method="POST", callback=self.parse)

    def parse(self, response):
        def check(lst, key):
            return lst[key] if key in lst else None

        data = json.loads(response.body)
        available_data = data['results'][0]['hits']
        total_pages = data['results'][0]['nbPages']

        mob_items = EmaxmeItems()

        for i in available_data:
            mob_items['color'] = check(i, 'color')
            mob_items['os'] = check(i, 'operatingSystem')
            mob_items['image'] = check(i,'primaryAssetContentUrl')
            mob_items['screenSize'] = check(i, 'screenSize')
            mob_items['currency'] = check(i, 'currency')
            mob_items['price'] = float(check(i,'price')) 
            mob_items['wasPrice'] = float(check(i, 'wasPrice'))
            mob_items['inStock'] = check(i, 'inStock')
            mob_items['name'] = i['name']['en']
            ram_rom = check(i,'capacity') 
            ram, rom = ram_rom.split(' ')[:2] if ' ' in ram_rom else [None, ram_rom]
            mob_items['ram'] = ram
            mob_items['rom'] = rom
            mob_items['url'] = self.allowed_domains[0] + check(i,'uri')
            mob_items['processor'] = check(i, 'processor')
            mob_items['page_num'] = self.go

            yield mob_items


        if self.go != total_pages:
            self.go+=1
            print(self.go)

            p = list(self.payload)
            p[86] = str(self.go)
            p = "".join(p)
            yield scrapy.Request(url=self.api_url, headers=self.h, body=p, method="POST", callback=self.parse)
