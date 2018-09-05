import scrapy
import logging
from .utils.spider_utils import ErrorReport

class DiscozSpider(scrapy.Spider):
    '''
    Brief: Implementation of a spider intended for scraping data from https://www.discogs.com/
    '''

    name = 'discogs'
    allowed_domains = 'discogs.com' # only parse discogs

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
        self._error_reports = []
        super(DiscozSpider, self).__init__(*args, **kwargs)

    def get_error_reports(self):
        return self._error_reports

    def _report_possible_error(self, url, component):
        '''
        Brief:      Reports suspitious data parsing value

        Param[in]:  url - Which page was being parsed

        Param[in]: component - What data was being extracted
        '''
        logging.warning("Possible error reported: URL = " + url + "; var = " + component)
        self._error_reports.append(ErrorReport(url, component))

    def parse_name(self, response):
        '''
        Brief:      Parses for the page title

        Param[in]:  Selector that contains the elements to parse
        '''
        res = response.xpath('//div[@class="profile"]/h1/spanitemprop/text()').extract()[0].strip()
        if res is None:
            self._report_possible_error(response.url, "Artists name")
        return res

    def parse_profile(self, selector):
        '''
        Brief:      Parses for the general info about the artist

        Param[in]:  Selector that contains the elements to parse
        '''
        pass


    def parse_track_list(self, selector):
        '''
        Brief:      Parses for the track list

        Param[in]:  Selector that ontains the elements to parse
        '''
        pass


    def parse_artist_page(self, response):
        '''
        Brief:   Parses the page containing information
                  that is of importance
        Details: Data to colect:
                    * Author
                    * Album name
                    * Country of origin
                    * Genre
                    * Style
        '''
        title = response.selector.xpath("//div[@class='profile']/h1")
        header_list = response.selector.xpath("//div[@class='profile']/div")
        content_list = response.selector.xpath("//div[@class='profile']/div")

        tracklist = response.selector.xpath("//div[@id='tracklist']")

    def start_requests(self):
        logging.info("Spider " + self.name + "started scraping for country " + self.get_country())
        yield scrapy.Request(url = self._url_base + self.get_country(), calbalck = self.parse)

    def parse(self, response):
        '''
        Brief: Parse the page for utls to follow
        '''
        for page in response.xpath('//a[@class="search_result_title"]'):
            yield response.follow(page, calbalck = self.parse_artist_page)

        logging.info(self.name + ": Acquiring next page to scrape")
        yield response.follow(response.xpath('//a[@class="pagination_next"]'), calbalck = self.parse)