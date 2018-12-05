import scrapy
import logging
import time

from disscoz_crawler.spiders.utils.error_report import ErrorReport
from disscoz_crawler.spiders.utils.spider_dispatcher import SpiderDispatcher
from disscoz_crawler.spiders.utils.spider_pool import SpiderPool
from disscoz_crawler.spiders.spider_factory.spider_factory import DiscozPageSpiderFactory
from disscoz_crawler.spiders.utils.dizcoz_db_driver import DiscozDBDriver
import time

# workaround
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import html2text

class ArtistData(scrapy.Item):
    '''
    Brief: Class holding the data to be sent to the spider pipeline
    '''
    name = scrapy.Field()
    profile = scrapy.Field()
    track_list = scrapy.Field()

class DiscozSpider(scrapy.Spider):
    '''
    Brief: Implementation of a spider intended for scraping data from https://www.discogs.com/

    Param [in]: country_to_scrape name of the country to scrape

    Param [in][optional]: error_recorder class used for reporting errors

    '''

    #download_delay = 1
    COOKIES_ENABLED = False
    ROBOTSTXT_OBEY = True

    name = 'discoz_spider'
    allowed_domains = ['discogs.com']

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

        self._db_driver = DiscozDBDriver()
        self._err_recorder = kwargs.get('error_recorder', None)
        super(DiscozSpider, self).__init__(*args, **kwargs)


    def set_country(self, country):
        self._country = country


    def get_country(self):
        return self._country


    def start_requests(self):
        logging.info("Spider " + self.name + "started scraping for country " + self.get_country())
        yield scrapy.Request(url = self._url_base + self.get_country(), callback=self.parse_discogz)


    def parse_discogz(self, response):
        '''
        Brief: Parse the page for urls to follow
        '''
        logging.info(self.name + ": Scraping the data page")
        for page in response.xpath('//a[@class="search_result_title"]/@href'):
            data_page = response.urljoin(page.extract())
            logging.info(self.name + ": Found an artist. Url: " + data_page)
            yield response.follow(page, callback=self.parse_artist_page_store_data)

        # next_page = response.urljoin(response.xpath('//a[@class="pagination_next"]')[0].extract())
        # logging.info(self.name + "Going to the next page: " + next_page)
        # yield response.follow(response.xpath('//a[@class="pagination_next"]')[0], callback = self.parse_discogz)

        print("Getting the error report:")
        if self._err_recorder is not None:
            print(self._err_recorder.get_error_reports())


    def parse_name(self, response):
        '''
        Brief:      Parses for the page title

        Param[in]:  Http response conataining the artist info page

        Returns:    The name of the artist
        '''
        logging.info(self.name + ": Parsing out the name...")
        res = None
        try:
            res = response.xpath('//div[@class="profile"]/h1/span[1]/span/a/text()').extract()[0].strip()
        except:
            logging.error(self.name + ": Couldn't parse the artist name")

        if res is None and self._err_recorder is not None:
            self._err_recorder.report_possible_error(response.url, "Artists name")

        return res


    def parse_profile(self, response):
        '''
        Brief:      Parses for the general info about the artist

        Param[in]:  Http response conataining the artist info page

        Returns:    Json containing the parsed data
        '''
        header_list = response.selector.xpath("//div[@class='profile']/div[@class='head']/text()").extract()
        content_selectors = response.selector.xpath("//div[@class='profile']/div[@class='content']")

        if len(header_list) != len(content_selectors):
            if self._err_recorder is not None:
                self._err_recorder.report_possible_error(response.url, "Profile data")
            return {}

        converter = html2text.HTML2Text()
        converter.ignore_links = True

        data = {}
        for i in range (0, len(content_selectors)):
            data[header_list[i].replace(':', '')] = str.strip( converter.handle(content_selectors[i].extract()))

        return data


    def parse_track_list(self, response):
        '''
        Brief:      Parses for the track list

        Param[in]:  Http response conataining the artist info page

        Returns:    List of the tracks performed by the artist
        '''

        data = response.selector.xpath("//span[@class='tracklist_track_title']/text()").extract()
        return data


    def parse_artist_page_store_data(self, response):
        '''
        Brief:      Parses the page containing information
                     that is of importance and stores it in the db

        Details:    Data to colect:
                       * Author
                       * Album name
                       * Country of origin
                       * Genre
                       * Style

        Param[in]:  Http response that contains the artists page to parse
        '''
        logging.info(self.name + ": Parsing an artist")

        data = ArtistData()

        data['name'] = self.parse_name(response)
        data['profile'] = self.parse_profile(response)
        data['track_list'] = self.parse_track_list(response)
        yield data # sending it off to the pipeline
        logging.info(self.name + ': Done parsing data for artist ' + data['name'])

