
from disscoz_crawler.spiders.spider_factory.spider_factory import DiscozPageSpiderFactory

import logging
from threading import Thread, Lock, Condition

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
        self._empty = Condition(self._mutex)

    def get_spider(self, is_blocking=True, timeout=None):
        '''
        Brief: makes a blocking or a nonblocking call
                to get a spider

        Param [in]: is_blocking should the call be blocking or not.
                        Default value is True

        Param [in/optional]: timeout if no spider is acquired
        '''
        if is_blocking:
            return self.get_spider_blocking(timeout)
        else:
            return self.get_spider_nonblocking()

    def get_spider_nonblocking(self):
        '''
        Brief: A nonblocking call that returns a spider

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

    def get_spider_blocking(self, timeout=None):
        '''
        Brief: A blocking call that returns a spider.
                Default setting is no timeout set

        Param [in/optional]: timeout if no spider is acquired

        Returns: a spider if successful, None if timeouted
        '''
        self._empty.acquire()
        try:
            if self._size != self._capacity:
                self._size = self._size + 1
                return self._spider_factory.create_spider()

            if timeout is not None:
                while self._head == -1:
                    # we will not return from this method if
                    # one notify came before timout but then we
                    # didn't acquire the lock, and we'll go back and with
                    # for time until notify + timeout. This is a minot bug,
                    # but we have no buget to deal with it
                    res = self._empty.wait(timeout)
                    if res is False:
                        logging.warning("Timedout on getting a spider!")
                        return None
            else:
                while self._head == -1:
                    self._empty.wait()

            cur_head = self._head
            self._head = self._head - 1
            return self._stack[cur_head]

        finally:
            self._empty.release()


    def put_spider(self, spider):
        '''
        Brief: Return spider to the pool
        '''
        self._mutex.acquire()
        try:
            self._head = self._head + 1
            self._stack[self._head] = spider
        finally:
            self._empty.notifyAll()
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
