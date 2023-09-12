from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

import scrapy
import json

from .lib.process_result import send_result_data


class PSPSpider(scrapy.Spider):
    name = 'psp'
    allowed_domains = ["psp.ge"]
    start_urls = ["https://psp.ge/category/823/products?page=1"]

    def parse(self, response):
        data = json.loads(response.text)
        result = []
        for item in data['data']['items']:
            price = item['price_range']['maximum_price']['final_price']['value']
            result.append({
                'name': item.get('name', ''),
                'price': int(price * 100),
                'pharmacy': 'Psp'
            })
        yield send_result_data(result)
        total_pages = data['data']['page_info']['total_pages']
        parsed_url = urlparse(response.request.url)
        query_params = parse_qs(parsed_url.query)
        cur_page = int(query_params.get('page', ['0'])[0])
        if cur_page < total_pages:
            query_params['page'] = [str(cur_page + 1)]
            parsed_url = parsed_url._replace(query=urlencode(query_params, doseq=True))
            url = urlunparse(parsed_url)
            yield response.follow(url, callback=self.parse)
