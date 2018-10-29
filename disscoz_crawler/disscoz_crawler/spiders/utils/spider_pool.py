
from disscoz_crawler.spiders.spider_factory.spider_factory import DiscozPageSpiderFactory

import logging
from threading import Thread, Lock

class SpiderPool():
    '''
    Brief: A pool of spiders lazy-created by the factory given in the constructor
    '''

    def __init__(self, spider_factory, pool_capacity=5):
        '''
        Brief: The constructor

        Param [in]: spider_factory factory used to create the spiders in the pool

        Param [in]: pool_capacity size of the spider pool
        '''
        self._spider_factory = spider_factory
        self._spiders_creted = 0
        self._capacity = pool_capacity
        self._stack = [None] * pool_capacity
        self._head = -1
        self._size = 0
        self._mutex = Lock()

    def get_spider(self):
        '''
        Brief: A call that returns a spider

        Returns: a spider if successful, None if not
        '''
        self._mutex.acquire()
        try:
            if self._head == -1:
                # queue is empty
                if self._size == self._capacity:
                    logging.warning("Spider pool capcaity reached!")
                    return None

                self._size = self._size + 1
                return self._spider_factory.create_spider()
            else:
                # return spider off the stack top
                cur_head = self._head
                self._head = self._head - 1
                return self._stack[cur_head]
        finally:
            self._mutex.release()

    def put_spider(self, spider):
        '''
        Brief: Return spider to the pool
        '''
        self._mutex.acquire()
        try:
            self._head = self._head + 1
            self._stack[self._head] = spider
        finally:
            self._mutex.release()

    def get_num_in_pool(self):
        '''
        Brief: Returns the current number of spiders in the pool
        '''
        self._mutex.acquire()
        try:
            return self._capacity - self._head - 1
        finally:
            self._mutex.release()
