import scrapy
import logging
import time

from disscoz_crawler.spiders.utils.error_report import ErrorReport
from disscoz_crawler.spiders.utils.dizcoz_db_driver import DiscozDBDriver

# workaround
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import html2text

class DiscozPageSpider(scrapy.Spider):
    '''
    Brief: Implementation of a spider intended for scraping data from https://www.discogs.com/ artist pages

    Param [in]: country_to_scrape name of the country to scrape

    Param [in][optional]: error_recorder class used for reporting errors

    '''
    _id = 0

    allowed_domains = ['www.discogs.com', 'discogs.com', 'http://www.discogs.com',
                        'https://www.discogs.com', '*'] # only parse discogs
    DOWNLOAD_DELAY = 1
    CONCURRENT_REQUESTS_PER_IP = 2

    def __init__(self, category=None, *args, **kwargs):
        '''
        Brief: Initializarion of the spider.
                country_to_scrape is a neccessary argument
        '''
        DiscozPageSpider._id = DiscozPageSpider._id + 1
        self.name = 'discoz_page_crawler_' + str(DiscozPageSpider._id)
        self._err_recorder = kwargs.get('error_recorder', None)
        super(DiscozPageSpider, self).__init__(*args, **kwargs)

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

    def parse_artist_page_store_data(self, response, db_driver):
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
        if db_driver is None:
            logging.error(self.name + ": No db driver is set!")
            return

        logging.info(self.name + ": Parsing an artist")
        name = self.parse_name(response)

        with db_driver() as db:
            if name is not None:
                logging.info(self.name + ": Storing a name")
                db.store_name(name)
