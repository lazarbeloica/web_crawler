import logging
from threading import Thread, Lock
from disscoz_crawler.spiders.utils.spider_pool import SpiderPool
from disscoz_crawler.spiders.discoz_page_spider import DiscozPageSpider

class SpiderDispatcher():
    '''
    Brief: Dispatches spiders on from the spider pool separate threads
            to do parsing jobs
    '''

    def __init__(self, spider_pool, db):
        '''
        Brief: Constructor

        Param [in]: spider_pool a pool to use for getting spiders

        Param [in]: db to be used
        '''
        self._db = db
        self._spider_pool = spider_pool
        self._active_threads = {}
        self._mutex = Lock()
        self._num_active_threads = 0

        logging.info("Created a spide dispatcher")

    def _generate_thread_name(self, spider):
        '''
        Brief: Generates the thread name from given spider
        '''
        return 'Thread' + spider.get_spider_name()

    def set_db_driver(self, db):
        '''
        Brief: sets a db driver to be used
        '''
        self._db = db

    def dispatch(self, request):
        '''
        Brief: Dispaches a spider to parse a given request

        Param [in]: request to be parsed by the spider
        '''
        spider = self._spider_pool.get_spider()
        spider.set_onfinished_callback(self.on_spider_finished)

        thread_name = self._generate_thread_name(spider)
        self._active_threads[thread_name] = Thread(name=thread_name, target=spider.parse_artist_page_store_data, args=(request,self._db))
        self._active_threads[thread_name].start()
        logging.debug(spider.get_spider_name() + "Spider dispatched!")

        self._mutex.acquire()
        self._num_active_threads = self._num_active_threads + 1
        self._mutex.release()

    def on_spider_finished(self, spider, thread_name):
        '''
        Brief: A callback to be used when the spider has finished it's work.
                It returns the spider to the pool and marks the thread as inactive in
                the list of used thread

        Param [in]: spider which called the callback

        Param [in]: thread_name on which the spider was running it's task
        '''
        self._mutex.acquire()
        try:
            self._spider_pool.put_spider(spider)
            self._active_threads[thread_name] = None
            logging.debug(spider.get_spider_name()+ " finished!")
        finally:
            self._num_active_threads = self._num_active_threads - 1
            self._mutex.release()

    def shut_down(self):
        '''
        Brief: Method to be called when shutting down the app.
                Waits for all the spiders to finish the current jobs
        '''
        for item in self._active_threads:
            item.join()
            self._mutex.acquire()
            self._num_active_threads = self._num_active_threads - 1
            self._mutex.release()

    def get_num_active_jobs(self):
        self._mutex.acquire()
        res = self._num_active_threads
        self._mutex.release()
        return res