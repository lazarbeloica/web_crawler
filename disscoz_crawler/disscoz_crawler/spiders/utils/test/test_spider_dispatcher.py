import unittest
from unittest.mock import MagicMock
import logging
import time
from disscoz_crawler.spiders.utils.spider_dispatcher import SpiderDispatcher

class TestSpiderPool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._spider_pool = MagicMock()
        self._spider = MagicMock()
        self._spider.get_spider_name.return_value = 'Test_spider'
        self._test_request = MagicMock()
        self._spider_pool.get_spider.return_value = self._spider

    def test_dispatch_single_spider(self):
        '''
        Brief: Tests dispatching a single spider
        '''
        dispatcher = SpiderDispatcher(self._spider_pool, None)
        dispatcher.dispatch(self._test_request)

        def mock_parse_artist_page_store_data(on_spider_finished):
            logging.debug("\n\nCalled")
            on_spider_finished(self._spider, 'Thread' + self._spider.get_spider_name())


        self._spider_pool.get_spider.assert_called_once()
        self._spider.set_onfinished_callback.assert_called_once_with(dispatcher.on_spider_finished)
        self._spider.parse_artist_page_store_data.assert_called_once_with(self._test_request, None)
        self._spider.parse_artist_page_store_data.return_value = mock_parse_artist_page_store_data((dispatcher.on_spider_finished))
        self.assertEqual(dispatcher.get_num_active_jobs(), 0)
