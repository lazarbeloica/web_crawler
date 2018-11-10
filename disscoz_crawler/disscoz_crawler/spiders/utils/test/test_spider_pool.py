import unittest
from unittest.mock import MagicMock
import logging
from threading import Thread, Lock
import time
from disscoz_crawler.spiders.utils.spider_pool import SpiderPool

class SpiderMock():
    pass

class TestSpiderPool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        '''
        Brief: Creates a mocked spider Factory
        '''
        self._spider_factory_mock = MagicMock()


    def test_get_spider(self):
        '''
        Brief: Tests getting a single spuder
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider(False))

    def test_get_spider_more_than_capacity(self):
        '''
        Brief: Tests getting more spiders than capacity
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider(False))
        self.assertTrue(pool.get_spider(False) == None, True)

    def test_get_put_get_spider(self):
        '''
        Brief: Getting a spider from pool cap=1, then putting it back and
                getting the same spider
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider(False))
        pool.put_spider(spider_mock)
        self.assertTrue(spider_mock, pool.get_spider(False))


    def test_get_spider_when_pool_empty(self):
        '''
        Brief: Getting spider from an empty pool
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider(False))
        self.assertTrue(None == pool.get_spider(False), True)


    def test_get_spider_when_capacity_zero(self):
        '''
        Brief: Getting spider from a pool that has cap = 0
        '''
        pool = SpiderPool(self._spider_factory_mock, 0)
        self.assertTrue(pool.get_spider(False) == None, True)

    def test_num_of_spiders_method(self):
        '''
        Brief: Tests calculating the number of spiders in the pool
        '''
        pool = SpiderPool(self._spider_factory_mock, 3)
        self.assertTrue(pool.get_num_in_pool(), 3)
        pool.get_spider(False)
        self.assertTrue(pool.get_num_in_pool(), 2)
        pool.get_spider(False)
        pool.get_spider(False)
        self.assertTrue(pool.get_num_in_pool(), 0)


    def test_get_spider_blocking(self):
        '''
        Brief: Tests getting a single spuder
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider())

    def test_get_put_get_spider_blocking(self):
        '''
        Brief: Getting a spider from pool cap=1, then putting it back and
                getting the same spider
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider())
        pool.put_spider(spider_mock)
        self.assertTrue(spider_mock, pool.get_spider())

    def test_get_spider_more_than_capacity_blocking(self):
        '''
        Brief: Tests getting more spiders than capacity
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider(True))
        self.assertTrue(pool.get_spider(True, 1) == None, True)

    def test_get_spider_when_pool_empty_blocking(self):
        '''
        Brief: Getting spider from an empty pool
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider(True, 1))
        self.assertTrue(None == pool.get_spider(True, 1), True)


    def test_get_spider_when_capacity_zero_blocking(self):
        '''
        Brief: Getting spider from a pool that has cap = 0
        '''
        pool = SpiderPool(self._spider_factory_mock, 0)
        self.assertTrue(pool.get_spider(True, 1) == None, True)

    def test_blocking_get_spider(self):
        '''
        Brief: Testing a blocking get_spider call until
                the spider is put from another thread
        '''
        mock_spider = SpiderMock()
        def run(spider_pool, spider):
            time.sleep(2)
            pool.put_spider(spider)

        pool = SpiderPool(self._spider_factory_mock, 1)
        self._spider_factory_mock.get_spider.return_value = mock_spider
        self.assertTrue(pool.get_spider(False), mock_spider)

        thread = Thread(target=run, args=(pool,mock_spider))
        thread.start()

        self.assertTrue(pool.get_spider(True), mock_spider)
        thread.join()
