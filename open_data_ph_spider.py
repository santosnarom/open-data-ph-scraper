import os
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
        self.keyword = keyword
        self.search_url = '{}?{}'.format(self.base_url, urlencode(params))

    def start_requests(self):
        yield Request(self.search_url, callback=self.handle_search_response)

    def handle_search_response(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        content_div = soup.find('div', attrs={'class': 'view-content'})

        if content_div:
            links = [header.a['href'] for header in content_div.find_all('h2')]
            for link in links:
                yield response.follow(link, callback=self.handle_dataset_page)

            next_page = soup.find('li', attrs={'class': 'pager-next'})
            if next_page:
                yield response.follow(next_page.a['href'], callback=self.handle_search_response)
        else:
            logging.warning('No results found for %s', self.keyword)

    def handle_dataset_page(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        # download all is not working so we'll use each file's download button instead
        dlinks = [i.parent['href'] for i in soup.find_all('i', attrs={'class': 'fa-download'})]

        # download all link is at the last index
        for dlink in dlinks[:-1]:
            yield response.follow(dlink, callback=self.save_file)

    def save_file(self, response):
        # save files to /tmp/opendataph for the meantime
        path = '/tmp/opendataph/'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        filename = response.url.rsplit('/', 1)[-1]
        filepath = '{}{}'.format(path, filename)
        with open(filepath, 'wb') as f:
            f.write(response.body)
