import unittest
from unittest.mock import MagicMock
from scrapy.http import HtmlResponse
import json
from disscoz_crawler.spiders.utils.spider_dispatcher import DiscozPageSpider
from disscoz_crawler.spiders.discoz_spider import DiscozSpider

class TestDiscozSpider(unittest.TestCase):

    TEST_PAGE = "/home/aviator/projects/tsz/src/web_crawler/disscoz_crawler/disscoz_crawler/spiders/test/test_page/serbia_page_discogs.html"

    @classmethod
    def setUpClass(self):
        self.mock_dispatcher = MagicMock()
        with open(self.TEST_PAGE, 'r') as myfile:
            body = myfile.read()
        self._response = HtmlResponse(url='http://test_page.fake', body=body, encoding='utf-8')


    def test_getting_links(self):
        spider = DiscozSpider(country_to_scrape='Serbia')
        spider.set_spider_dispatcher(self.mock_dispatcher)
        pass
