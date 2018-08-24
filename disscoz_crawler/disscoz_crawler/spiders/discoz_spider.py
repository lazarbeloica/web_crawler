import scrapy

class DiscozSpider(scrapy.Spider):
    '''
    Brief: Implementation of a spider intended for scraping data from https://www.discogs.com/
    '''

    name = 'discogs'
    allowed_domains = 'discogs.com' # only parse discogs
    start_urls = ['https://www.discogs.com/']

    def parse(self, response):
        '''
        Brief: Parse the home page
        '''