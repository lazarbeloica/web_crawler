import unittest
from scrapy.http import HtmlResponse
from disscoz_crawler.disscoz_crawler.spiders.discoz_spider import DiscozSpider

class TestDiscozSpider(unittest.TestCase):
    '''
    '''

    TEST_PAGE = "/home/aviator/projects/tsz/src/web_crawler/disscoz_crawler/disscoz_crawler/spiders/test/test_page/pr.html"

    @classmethod
    def setUpClass(self):
        '''
        Details: Creates a response that contains a discoz.com page that will be used for all tests.
        '''
        self.spider = DiscozSpider(country_to_scrape='Serbia')
        with open(self.TEST_PAGE, 'r') as myfile:
            body = myfile.read()
        self._response = HtmlResponse(url='http://test_page.fake', body=body, encoding='utf-8')


    def test_title_name(self):
        self.assertEqual("Neško Kejdž", self.spider.parse_name(self._response))

    def test_profile_data(self):
        pass

    def test_track_list(self):
        pass

    def test_parse_page(self):
        pass

