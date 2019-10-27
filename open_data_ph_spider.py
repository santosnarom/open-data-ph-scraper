import logging
from urllib.parse import urlencode

from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider


class OpenDataPhSpider(Spider):
    name = 'open_data_ph_spider'
    base_url = 'https://data.gov.ph/'

    def __init__(self, keyword=None, ext=None, *args, **kwargs):
        if not keyword:
            logging.error('Please provide a search keyword')
            raise CloseSpider()

        super(OpenDataPhSpider, self).__init__(*args, **kwargs)
        params = {'q': 'search', 'query': keyword}
        self.search_url = '{}?{}'.format(self.base_url, urlencode(params))

    def start_requests(self):
        yield Request(self.search_url, callback=self.handle_initial_response)

    def handle_initial_response(self, response):
        from scrapy.utils.response import open_in_browser
        open_in_browser(response)
