from disscoz_crawler.spiders.discoz_page_spider import DiscozPageSpider

class DiscozPageSpiderFactory():
    '''
    Brief: Interface used for creating spiders
    '''

    def __init__(self, **kwargs):
        '''
        Brief: Constructor

        Param [in/optional]: error_recorder to be passed on
                            to every spider created
        '''
        self._error_recorder = kwargs.get('error_recorder', None)

    def create_spider(self):
        '''
        Brief: Returns an instance of a Discgz page spider
        '''
        if self._error_recorder is not None:
            return DiscozPageSpider(error_recorder=self._error_recorder)
        else:
            return DiscozPageSpider()

