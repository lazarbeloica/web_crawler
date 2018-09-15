import scrapy
import logging

from disscoz_crawler.disscoz_crawler.spiders.utils.spider_utils import ErrorReport

# workaround
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import html2text

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

        Param[in]:  Http response conataining the artist info page

        Returns:    The name of the artist
        '''
        res = response.xpath('//div[@class="profile"]/h1/spanitemprop/text()').extract()[0].strip()
        if res is None:
            self._report_possible_error(response.url, "Artists name")
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
            self._report_possible_error(response.url, "Profile data")
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
        pass


    def start_requests(self):
        logging.info("Spider " + self.name + "started scraping for country " + self.get_country())
        yield scrapy.Request(url = self._url_base + self.get_country(), calbalck = self.parse)

    def parse(self, response):
        '''
        Brief: Parse the page for urls to follow
        '''
        for page in response.xpath('//a[@class="search_result_title"]'):
            yield response.follow(page, calbalck = self.parse_artist_page_store_data)

        logging.info(self.name + ": Acquiring next page to scrape")
        yield response.follow(response.xpath('//a[@class="pagination_next"]'), calbalck = self.parse)