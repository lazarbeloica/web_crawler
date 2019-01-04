import scrapy
import logging
import time
import re

from disscoz_crawler.spiders.utils.error_report import ErrorReport
from disscoz_crawler.spiders.utils.spider_dispatcher import SpiderDispatcher
from disscoz_crawler.spiders.utils.spider_pool import SpiderPool
from disscoz_crawler.spiders.spider_factory.spider_factory import DiscozPageSpiderFactory
from disscoz_crawler.spiders.utils.dizcoz_db_driver import DiscozDBDriver
import time
from datetime import datetime

# workaround
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import html2text

logging.getLogger().setLevel(logging.INFO)

class ArtistData(scrapy.Item):
    '''
    Brief: Class holding the data to be sent to the spider pipeline
    '''
    artist_name = scrapy.Field()
    album_name = scrapy.Field()
    profile = scrapy.Field()
    track_list = scrapy.Field()
    album_version = scrapy.Field()
    album_rating = scrapy.Field()
    album_credits = scrapy.Field()

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

        next_page = response.urljoin(response.xpath('//a[@class="pagination_next"]')[0].extract())
        logging.info(self.name + "Going to the next page: " + next_page)
        yield response.follow(response.xpath('//a[@class="pagination_next"]')[0], callback = self.parse_discogz)


    def _clense_name(self, name):
        return re.sub('\([0-9]+\)','',name).strip()


    def parse_artist_name(self, response):
        '''
        Brief:      Parses for the artists name

        Param[in]:  Http response conataining the artist info page

        Returns:    The name of the artist
        '''
        logging.info(self.name + ": Parsing out the artist name...")
        res = None
        try:
            res = response.xpath('//div[@class="profile"]/h1/span[1]/span/a/text()').extract()[0].strip()
        except:
            logging.error(self.name + ": Couldn't parse the artist name")

        if res is None and self._err_recorder is not None:
            self._err_recorder.report_possible_error(response.url, "Artists name")

        return self._clense_name(res)


    def parse_album_name(self, response):
        '''
        Brief:      Parses for the album

        Param[in]:  Http response conataining the artist info page

        Returns:    The name of the album
        '''
        logging.info(self.name + ": Parsing out the album name...")
        res = None
        try:
            res = response.xpath('//div[@class="profile"]/h1/span[2]/text()').extract()[0].strip()
        except:
            logging.error(self.name + ": Couldn't parse the album name")

        if res is None and self._err_recorder is not None:
            self._err_recorder.report_possible_error(response.url, "Album name")

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

        Returns:    List of the tracks performed by the artist and duration of each track
        '''
        tracklist_selectors = response.selector.xpath("//tr[@class=' tracklist_track track']")
        tracklist_selectors.append(response.selector.xpath("//tr[@class='first tracklist_track track']"))

        data = []
        for selector in  tracklist_selectors:
            title = selector.xpath("./td[@class='track tracklist_track_title '] |  ./td[@class='track tracklist_track_title mini_playlist_track_has_artist']").xpath("./a/span/text() | ./span/text()").extract()
            duration = selector.xpath("./td[@class='tracklist_track_duration']/span/text()").extract()
            if duration != []:
                duration = [datetime.strptime(duration[0].strip(), '%M:%S')]
            else:
                duration = None

            data.append([title[0].strip(), duration])

        return data


    def parse_album_versions(self, response):
        versions = len(response.selector.xpath('//table[@id="versions"]/tr'))
        return (1 if versions == 0 else versions - 1)


    def _role_matcher(self, pattern, roles, selector):
        '''
        Brief: Mathes the pattern in given roles list and returns the
                list of elements from the selector that corispond to the matched role
        '''
        if roles == []:
            return []

        regex = re.compile(pattern, re.IGNORECASE)
        if regex.search(roles):
            person = selector.xpath("./a[@class='rollover_link']/text()").extract()
            return person

        return []


    def parse_credits(self, response):
        '''
        Brief: Parses for data in Credits such as Vocals, Wirting & Arangmants

        Returns: json with parsed data
        '''
        arangmants = []
        writters = []
        vocals = []
        for selector in response.selector.xpath("//ul[@class='list_no_style']/li"):
            roles = selector.xpath("./span[@class='role']/text()").extract()
            roles = roles[0] if roles != [] else ""

            res = self._role_matcher('vocals', roles, selector)
            vocals = vocals + res

            res = self._role_matcher('written', roles, selector)
            writters = writters + res

            res = self._role_matcher('arranged', roles, selector)
            arangmants = arangmants + res

        return {'vocals': vocals, 'writting': writters, 'arranging': arangmants}

    def parse_rating(self, response):
        '''
        Brief: Parses for album rating

        Returns: Album rating aout of 5
        '''
        rating = response.selector.xpath("//span[@class='rating_value']/text()").extract()[0]
        try:
            rating = float(rating)
        except:
            rating = 0

        return rating


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

        data['artist_name'] = self.parse_artist_name(response)
        data['album_name'] = self.parse_album_name(response)
        data['profile'] = self.parse_profile(response)
        data['album_version'] = self.parse_album_versions(response)
        data['track_list'] = self.parse_track_list(response)
        data['album_rating'] = self.parse_rating(response)
        data['album_credits'] = self.parse_credits(response)
        yield data # sending it off to the pipeline
        logging.info(self.name + ': Done parsing data for artist ' + data['artist_name'])

