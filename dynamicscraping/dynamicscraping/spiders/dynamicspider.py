from typing import Iterable
from ..items import DynamicscrapingItem
import scrapy, json

from scrapy.http import Response

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

class DynamicspiderSpider(scrapy.Spider):
    name = "dynamicspider"
    allowed_domains = ["directory.ntschools.net"]
    # start_urls = ["https://directory.ntschools.net/#/schools"]
    api_url = 'https://directory.ntschools.net/api/System/GetAllSchools'

    h = get_headers('''
                    accept: application/json
                    accept-encoding: gzip, deflate, br, zstd
                    accept-language: en-US,en;q=0.9
                    cache-control: no-cache
                    connection: keep-alive
                    host: directory.ntschools.net
                    pragma: no-cache
                    referer: https://directory.ntschools.net/
                    sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
                    sec-ch-ua-mobile: ?0
                    sec-ch-ua-platform: "Windows"
                    sec-fetch-dest: empty
                    sec-fetch-mode: cors
                    sec-fetch-site: same-origin
                    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
                    x-requested-with: Fetch
                    ''')


    def start_requests(self):
        
        yield scrapy.Request(url=self.api_url, headers=self.h, callback=self.parse)

    def parse(self, response):
        print(response.url)
        base_url = 'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode='
        raw_data = response.body    # string
        print(raw_data)
        data = json.loads(raw_data) # json

        for school in data:
            school_url = base_url + school['itSchoolCode']
            yield scrapy.Request(url=school_url, callback=self.school_parse, headers=self.h)

    def school_parse(self, response):

        data_items = DynamicscrapingItem()
        raw_data = response.body    # string
        data = json.loads(raw_data) # json

        data_items['name'] = data['name']
        data_items['physicalAddress'] = data['physicalAddress']['displayAddress']
        data_items['postalAddress'] = data['postalAddress']['displayAddress']
        data_items['email'] = data['mail']
        data_items['phone'] = data['telephoneNumber']
        data_items['url'] = response.url
        yield data_items


