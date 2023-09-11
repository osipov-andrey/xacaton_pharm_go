import scrapy
from scrapy.http import JsonRequest
import re
import json


class MedscrapperSpider(scrapy.Spider):
    name = "medscrapper"
    allowed_domains = ["www.aversi.ge"]
    start_urls = ["https://www.aversi.ge/en/medikamentebi"]

    def parse(self, response):
        cats = response.css('.panel-content')
        for cat in cats:
            link = cat.css('a').attrib['href']
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        items = response.css('.product-details')
        data = []
        for item in items:
            price_text = item.css('.amount::text').get()
            price_text = re.search(r'(\d+\.\d+)', price_text).group()
            try:
                price = float(price_text)
            except:
                price = 0
            name = item.css('.product-title::text').get().replace(' ', '_').replace('#', '')
            data.append({
                'name': name,
                'price': int(price*100),
                'pharmacy': 'Aversi'
            })
        json_payload = json.dumps(data)

        # print(json_payload)
        headers = {
            'Content-Type': 'application/json',
        }

        request = JsonRequest(
            url='http://192.168.10.104:5005/med',
            headers=headers,
            method='POST',
            data=data,
            dont_filter=True,
            callback=self.parse_json_response
        )
        yield request
        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_category)

    def parse_json_response(self, response):
        try:
            data = json.loads(response.text)
            # Process the JSON data here
            self.logger.info(data)
        except json.JSONDecodeError as e:
            self.logger.error(f'Error decoding JSON response: {str(e)}')
