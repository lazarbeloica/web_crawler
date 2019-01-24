import scrapy
import logging

from disscoz_crawler.items import ResponseData

logging.getLogger().setLevel(logging.INFO)


class DiscozSpider(scrapy.Spider):
    '''
    Brief: Implementation of a spider intended for scraping data from https://www.discogs.com/

    Param [in]: country_to_scrape name of the country to scrape

    Param [in][optional]: error_recorder class used for reporting errors

    '''

    download_delay = 1
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

        next_page = response.urljoin(response.xpath('//a[@class="pagination_next"]')[0].extract())
        logging.info(self.name + "Going to the next page: " + next_page)
        yield response.follow(response.xpath('//a[@class="pagination_next"]')[0], callback = self.parse_discogz)


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
        data = ResponseData()
        data['response'] = response
        yield data # sending it off to the pipeline

