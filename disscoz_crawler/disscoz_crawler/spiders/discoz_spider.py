import scrapy
import logging
import time

from disscoz_crawler.spiders.utils.error_report import ErrorReport
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

    name = 'discoz'
    allowed_domains = ['www.discogs.com', 'discogs.com', 'http://www.discogs.com',
                        'https://www.discogs.com', '*'] # only parse discogs
    DOWNLOAD_DELAY = 1
    CONCURRENT_REQUESTS_PER_IP = 2

    _url_base = 'https://www.discogs.com/search/?country_exact='

    def set_country(self, country):
        self._country = country

    def get_country(self):
        return self._country

    def __init__(self, category=None, *args, **kwargs):
        '''
        Brief: Initializarion of the spider.
                country_to_scrape is a neccessary argument
        '''
        country = kwargs.get('country_to_scrape', None)
        if country is not None:
            self.set_country(country)
        elif self.get_country() is None:
            logging.error(self.name + ': No country is given')
            raise Exception(self.name + ': No country is given')

        self._err_recorder = kwargs.get('error_recorder', None)
        super(DiscozSpider, self).__init__(*args, **kwargs)

    def parse_name(self, response):
        '''
        Brief:      Parses for the page title

        Param[in]:  Http response conataining the artist info page

        Returns:    The name of the artist
        '''
        logging.info("Parsing out the name...")
        res = response.xpath('//div[@class="profile"]/h1/spanitemprop/text()').extract()[0].strip()
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
        tracklist_selectors = response.selector.xpath("//tbody/tr/td[@class='track tracklist_track_title ']/a")

        converter = html2text.HTML2Text()
        converter.ignore_links = True

        data = []
        for i in range (0, len(tracklist_selectors)):
            data.append(str.strip(converter.handle(tracklist_selectors[i].extract())))

        return data

    def parse_artist_page_store_data(self, response, db):
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
        logging.info(self.name + ": Parsing an artist - 2")
        name = self.parse_name(response)
        if name is not None:
            logging.info(self.name + ": Storing a name")
            db.store_name(name)

    def start_requests(self):
        logging.info("Spider " + self.name + "started scraping for country " + self.get_country())
        yield scrapy.Request(url = self._url_base + self.get_country(), callback=self.parse)

    def parse(self, response):
        '''
        Brief: Parse the page for urls to follow
        '''
        logging.info(self.name + ": Scraping the data page")
        for page in response.xpath('//a[@class="search_result_title"]/@href'):
            logging.info(self.name + ": Found an artist")
            next_page = response.urljoin(page.extract())
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse_artist_page_store_data)

#        yield scrapy.Request(response.xpath('//a[@class="pagination_next"]')[0], callback = self.parse)

        print("Getting the error report:")
        if self._err_recorder is not None:
            print(self._err_recorder.get_error_reports())
