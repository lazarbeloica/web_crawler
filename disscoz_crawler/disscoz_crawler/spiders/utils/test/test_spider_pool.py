import unittest
from unittest.mock import MagicMock
import logging
from threading import Thread, Lock

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
        pass


    def test_get_spider(self):
        '''
        Brief: Tests getting a single spuder
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider())

    def test_get_spider_more_than_capacity(self):
        '''
        Brief: Tests getting more spiders than capacity
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider())
        self.assertTrue(pool.get_spider() == None, True)

    def test_get_put_get_spider(self):
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


    def test_get_spider_when_pool_empty(self):
        '''
        Brief: Getting spider from an empty pool
        '''
        spider_mock = SpiderMock()
        self._spider_factory_mock.get_spider.return_value = spider_mock
        pool = SpiderPool(self._spider_factory_mock, 1)
        self.assertTrue(spider_mock, pool.get_spider())

    def test_get_spider_when_capacity_zero(self):
        '''
        Brief: Getting spider from a pool that has cap = 0
        '''
        pool = SpiderPool(self._spider_factory_mock, 0)
        self.assertTrue(pool.get_spider() == None, True)

    def test_num_of_spiders_method(self):
        '''
        Brief: Tests calculating the number of spiders in the pool
        '''
        pool = SpiderPool(self._spider_factory_mock, 3)
        self.assertTrue(pool.get_num_in_pool(), 3)
        pool.get_spider()
        self.assertTrue(pool.get_num_in_pool(), 2)
        pool.get_spider()
        pool.get_spider()
        self.assertTrue(pool.get_num_in_pool(), 0)

