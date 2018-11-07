from disscoz_crawler.spiders.discoz_page_spider import DiscozPageSpider

class DiscozPageSpiderFactory():
    '''
    Brief: Interface used for creating spiders
    '''

    def create_spider(self):
        '''
        Brief: Returns an instance of a Discgz page spider
        '''
        return DiscozPageSpider()

