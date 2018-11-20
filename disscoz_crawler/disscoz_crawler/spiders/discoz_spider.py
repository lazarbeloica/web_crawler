import scrapy
import logging
import time

from disscoz_crawler.spiders.utils.error_report import ErrorReport
from disscoz_crawler.spiders.utils.spider_dispatcher import SpiderDispatcher
from disscoz_crawler.spiders.utils.spider_pool import SpiderPool
from disscoz_crawler.spiders.spider_factory.spider_factory import DiscozPageSpiderFactory
from disscoz_crawler.spiders.utils.dizcoz_db_driver import DiscozDBDriver

# workaround
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import html2text

class DiscozSpider(scrapy.Spider):
    '''
    Brief: Implementation of a spider intended for scraping data from https://www.discogs.com/

    Param [in]: country_to_scrape name of the country to scrape

    Param [in][optional]: error_recorder class used for reporting errors

    '''

    name = 'discoz_spider'
    allowed_domains = ['www.discogs.com', 'discogs.com', 'http://www.discogs.com',
                        'https://www.discogs.com', '*']
    DOWNLOAD_DELAY = 1
    CONCURRENT_REQUESTS_PER_IP = 2

    _url_base = 'https://www.discogs.com/search/?country_exact='

    def __init__(self, category=None, *args, **kwargs):
        '''
        Brief: Initializarion of the spider.
                country_to_scrape is a neccessary argument
                spider dispacther and db driver will be created
                    with default values. It is possible tochange this later
        '''
        country = kwargs.get('country_to_scrape', None)
        if country is not None:
            self.set_country(country)
        elif self.get_country() is None:
            logging.error(self.name + ': No country is given')
            raise Exception(self.name + ': No country is given')

        self._spider_dispatcher = SpiderDispatcher(SpiderPool(DiscozPageSpiderFactory()), DiscozDBDriver())
        self._err_recorder = kwargs.get('error_recorder', None)
        super(DiscozSpider, self).__init__(*args, **kwargs)

    def set_country(self, country):
        self._country = country

    def get_country(self):
        return self._country

    def set_spider_dispatcher(self, dispatcher):
        '''
        Brief: Sets a spider dispatcher to be used
        '''
        self._spider_dispatcher = dispatcher

    def start_requests(self):
        logging.info("Spider " + self.name + "started scraping for country " + self.get_country())
        yield scrapy.Request(url = self._url_base + self.get_country(), callback=self.parse)

    def parse(self, response):
        '''
        Brief: Parse the page for urls to follow
        '''
        logging.info(self.name + ": Scraping the data page")
        for page in response.xpath('//a[@class="search_result_title"]/@href'):
            data_page = response.urljoin(page.extract())
            logging.info(self.name + ": Found an artist. Url: " + data_page)
            yield scrapy.Request(data_page, callback=self._spider_dispatcher.dispatch)

        next_page = response.urljoin(response.xpath('//a[@class="pagination_next"]')[0].extract())
        logging.info(self.name + "Going to the next page: " + next_page)
        yield scrapy.Request(next_page, callback = self.parse)

        logging.info(self.name + ": All done indexing... Waiting for page parsing to be done...")
        self._spider_dispatcher.shut_down()

        print("Getting the error report:")
        if self._err_recorder is not None:
            print(self._err_recorder.get_error_reports())
