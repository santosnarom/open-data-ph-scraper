import logging
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider


class OpenDataPhSpider(Spider):
    name = 'open_data_ph_spider'
    base_url = 'https://data.gov.ph/'

    def __init__(self, keyword=None, *args, **kwargs):
        if not keyword:
            logging.error('Please provide a search keyword')
            raise CloseSpider()

        super(OpenDataPhSpider, self).__init__(*args, **kwargs)
        params = {'q': 'search', 'query': keyword}
        self.search_url = '{}?{}'.format(self.base_url, urlencode(params))

    def start_requests(self):
        yield Request(self.search_url, callback=self.handle_search_response)

    def handle_search_response(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        result_div = soup.find('div', attrs={'class': 'search-result-dataset'})

        if result_div:
            links = [header.a['href'] for header in result_div.find_all('h2')]
            for link in links:
                yield response.follow(link, callback=self.handle_dataset_page)
        else:
            logging.warning('No results found for %s', self.keyword)

    def handle_dataset_page(self, response):
        from scrapy.utils.response import open_in_browser; open_in_browser(response)
        import pdb; pdb.set_trace()
