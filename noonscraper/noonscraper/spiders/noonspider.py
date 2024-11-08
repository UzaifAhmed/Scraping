from typing import Iterable
import scrapy
from ..items import PhoneProducts

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

class NoonspiderSpider(scrapy.Spider):
    name = "noonspider"
    allowed_domains = ["www.noon.com"]
    start_urls = ["https://www.noon.com/uae-en/electronics-and-mobiles/mobiles-and-accessories/mobiles-20905/?limit=150"]
    counter = 1

    def start_requests(self):
        #   Only User Agent is not enough then we send complete Header
        h = get_headers('''
                        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
                        accept-encoding: gzip, deflate, br, zstd
                        accept-language: en-US,en;q=0.9
                        cache-control: max-age=0
                        cookie: nloc=en-ae; visitor_id=c34a78f1-a339-4fdd-9d63-b80e5a33e39a; _gcl_au=1.1.2051819879.1727081670; _ga=GA1.2.2017405328.1727081672; _gid=GA1.2.1866090762.1727081672; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22JHAZtGnwGCx0xslmHVOs%22%7D; _scid=eHIvyrjogGMABf-a3OQZGISH60TTPLAY; _ym_uid=1727081672868382408; _ym_d=1727081672; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3Anull%7D; _fbp=fb.1.1727081672783.383319568503528629; ZLD887450000000002180avuid=472d1742-ac81-4960-b499-6358c142bffa; _ScCbts=%5B%5D; _tt_enable_cookie=1; _ttp=0lEH_R5HuYVOi87iqjOIkPNrlGe; __gads=ID=e8c38aa4f8ec4c4f:T=1727081672:RT=1727081672:S=ALNI_MYbGV_XEOMGAwzHEl35LLmb0bCWXQ; __gpi=UID=00000f097a30acbf:T=1727081672:RT=1727081672:S=ALNI_MaTAk3yMFwz-3zVQvxKjh6FpT2nJA; __eoi=ID=1174fecb8fc9973e:T=1727081672:RT=1727081672:S=AA-AfjZFoj5WxcDi-FoL7eJwzxsw; _clck=sxlp8y%7C2%7Cfpf%7C0%7C1727; _sctr=1%7C1727031600000; review_lang=xx; AKA_A2=A; _etc=xJwP3Do69DS4WeWV; nguestv2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJraWQiOiIxMDFlZjRiMzUwNzk0ZWE2YmQwODVhZjQzZWE4MmNlYyIsImlhdCI6MTcyNzA4OTE0MywiZXhwIjoxNzI3MDg5NDQzfQ.x3U9gBXOy4ohKU7ET_p4x8t-romQ2JUf_QJbyNt0phg; ak_bmsc=BBA3A81552AA9292AB1C5E5E3C9C1619~000000000000000000000000000000~YAAQPuUcuIaIUA6SAQAAPPKIHhnykc7HO43nAvOAsfz5TsW1/AivP2j12TLjFBODXdvbR+QiiZ/mxVMt6Q003SWWdM7QogpL+uo9NRTqPjtGYYfTT3qqph3jRB68ufsE6SIxUkxGIQV4A5nS95EXuhqE5pLsnvfgRqH6f2l2yfWiKVvXzWIJKzyD4yDE3bY+8Fv/gq5dm+7/uDWsTV7NyvfGpJXunu90Sv4k8rod1GOswjGsHapY8nZ4rj5H/8G0WTeWQgJIFTmf6WUu89tOKi9P+awMv6hWtHrGNOOkbeHsn7HamPm9fWjKL8wgtTjbLngxyAIyKmZTkSrmC30kSgWVGRFovlThgEbg7WUiO9UAime/mJmTLekcKliBjXbLG/NV4g18TECO8mjQCls54PXQj2CzP2S3G6JcXUGCsY81JheoGi0iwPugQRwQyw56pp28Q3OLjPEBH1j+; _scid_r=hPIvyrjogGMABf-a3OQZGISH60TTPLAYl9wmWg; _uetsid=73986250798911efa956e54281283d56; _uetvid=7398d0e0798911efafbd6b04c2fee2e6; bm_sv=4AE98DB0E69BB9E65AC4FB004C2C5395~YAAQPuUcuGuJUA6SAQAAkxyJHhkIzEQxLMLnKhsZXzXJsPv4wLwO8YI/CzQ3A8KkwG/r1mm+MixU7y+cq9VijNDoECtpVZqRy1tWMZ361oknZeh3yPkvSikDvFUzSq66+DV5dbhyvzb+smeM4iD2xV1Ec71ToWRQ+Rk96HD+UFssiaxOFeE8qfYsMm2y2Y9RwqWFw7k9NslR3ddiZlKrRKld3lhespd8rSclm01kyUILlsx1gv+9k/yL6mPw5A==~1; _clsk=1mo7kuc%7C1727091179095%7C1%7C0%7Co.clarity.ms%2Fcollect; ZLDsiq3b3ce696144e42ab351af48092266ce3dda2b3c7b2ad6e09ba5d18504de03180tabowner=undefined; RT="z=1&dm=noon.com&si=8761cec6-d58d-42f3-a76e-d04df3617d35&ss=m1ewa3qi&sl=0&tt=0&ul=18fvi"
                        priority: u=0, i
                        sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"
                        sec-ch-ua-mobile: ?0
                        sec-ch-ua-platform: "Windows"
                        sec-fetch-dest: document
                        sec-fetch-mode: navigate
                        sec-fetch-site: same-origin
                        sec-fetch-user: ?1
                        upgrade-insecure-requests: 1
                        user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36
                        ''')
        
        yield scrapy.Request(self.start_urls[0], headers=h, callback=self.parse)

    def parse(self, response):
        # Mobiles page
        url = response.xpath('//*[@class="sc-19767e73-0 bwele"] //a/@href').getall()

        # Page Number
        pg = response.css('li.active a::text').extract()[0]

        # All mobiles in this page
        for mobile in url:
            yield scrapy.Request('https://www.noon.com' + mobile, callback=self.parse_mobiles, meta={'pg':pg})

        # If click next is disabled
        next_disabled = response.css('li.next a::attr(aria-disabled)').extract()[0]

        # switching page
        self.counter+=1
        if next_disabled == 'false':
            url = response.url.split('&')[0] if '&' in response.url else response.url
            next_page_url = url + '&page=' + str(self.counter) + '&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc'

            yield scrapy.Request(next_page_url, callback=self.parse)

        

    def parse_mobiles(self, response):
        def check(key):
            specifications = response.css('div.sc-966c8510-2 td::text').getall()
            return specifications[specifications.index(key)+1] if key in specifications else None
            
        # def availab(itm, key, ind):
        #     if key:
        #         itm[key] = key[ind]

        mobile_item = PhoneProducts()

        name = response.css('h1.sc-b74d844-17::text').extract()
        if name:
            mobile_item['name'] = name[0]
        else:
            mobile_item['name'] = ''
        
        pricing = response.css('div.priceNow::text').extract()
        if pricing:
            mobile_item['currency'] = pricing[0]
        else:
            mobile_item['currency'] = ''
        

        # if offer is None
        if len(response.css('span.profit')) == 0 and pricing:
            mobile_item['offer_price'] = None
            mobile_item['regular_price'] = float(pricing[2])

        else:
            if pricing:
                mobile_item['offer_price'] = float(pricing[2])

                reg_price = response.css('div.priceWas::text').extract()
                if reg_price:
                    mobile_item['regular_price'] = float(response.css('div.priceWas::text').extract()[2])
                else:
                    mobile_item['regular_price'] = 0

            

        mobile_item['colour'] = check('Colour Name')
        mobile_item['ram'] = check('RAM Size')
        mobile_item['rom'] = check('Internal Memory')
        mobile_item['os_version'] = check('Operating System Version')
        mobile_item['processor'] = check('Processor Name')
        mobile_item['url'] = response.url

        # img_url = response.css('div.section img').attrib['src']
        # mobile_item['image'] = None if len(img_url) == 0 else img_url
        try:
            img_url = response.css('div.section img').attrib['src']
        except:
            img_url = None
        mobile_item['image'] = img_url
        mobile_item['page_number'] = response.meta['pg']

        yield mobile_item

