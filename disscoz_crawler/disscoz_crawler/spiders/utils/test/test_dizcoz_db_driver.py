import logging
import unittest
from disscoz_crawler.spiders.utils.dizcoz_db_driver import DiscozDBDriver

class TestDiscozDBDriver(unittest.TestCase):

    def test_connection(self):
        '''
        Brief: Test if we can querry the db
        '''
        try:
            db = DiscozDBDriver()
            db._connect()
            db.custom_query("SELECT * from artist")
            db._disconnect
        except:
            assert False, "No DB connection"
