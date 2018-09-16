import unittest
from scrapy.http import HtmlResponse
import json
from disscoz_crawler.spiders.discoz_spider import DiscozSpider

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
        expected = json.loads(""" {
            "Label": "PGP RTS ‎– CD 407239",
            "Format" : "CD, Album",
            "Country" : "Serbia",
            "Released" : "2006",
            "Genre" : "Pop, Folk, World, & Country",
            "Style" : ""
        } """ )

        self.assertTrue(expected == self.spider.parse_profile(self._response))


    def test_track_list(self):
        expected = ['Kada Mi Se Dogodiš',
        'Votka I Džin',
        'Opako',
        'Nije Meni Suđeno',
        'Santa Leda',
        'Sve Mi Ide Naopako',
        'Doživotno',
        'Zavistan',
        'Želiš Mi Sreću',
        'Ako Me Varaš']

        self.assertEqual(expected, self.spider.parse_track_list(self._response))

    def test_parse_page(self):
        self.spider.parse_artist_page_store_data(self._response)

