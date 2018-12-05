# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import MySQLdb

class DisscozCrawlerDBPipeline(object):

    db_info = {"user" : "root",
            "psw" : "LakiBel944",
            "host" : "127.0.0.1",
            "db" : "discoz"
            }

    count = 0

    def _connect(self):
        self._db = MySQLdb.connect(host=self.db_info["host"],
                     user=self.db_info["user"],
                     passwd=self.db_info["psw"],
                     db=self.db_info["db"])

        logging.info("DB: Conected")
        self._cursor = self._db.cursor()

        self._db.set_character_set('utf8')
        self._cursor.execute('SET NAMES utf8;')
        self._cursor.execute('SET CHARACTER SET utf8;')
        self._cursor.execute('SET character_set_connection=utf8;')


    def _disconnect(self):
        self._db.close()
        logging.info("DB: Disconected")


#    def __enter__(self):
#        self._connect()
#        return self
#
#
#    def __exit__(self,exc_type, exc_value, traceback):
#        self._disconnect()


    def store_name(self, name):
        try:
            logging.debug('DB: Storing name ' + name)
            self._cursor.execute("""INSERT INTO artist (artist_name) VALUES (%s); """, (name,))
            self._db.commit()

            self._cursor.execute("""select id from artist where artist_name = %s""" , (name,))
            artist_id = self._cursor.fetchone()
            return artist_id[0]
        except:
            self._db.rollback()
            logging.error('Artist already in db - ' + name)
            return None


    def store_profile(self, profile, artist_id):
        logging.info("DB: Stioring artist profile to db")
        for trate in profile:
            try:
                query_data = [artist_id, trate, profile[trate]]
                logging.debug('DB: Storing trate ' + trate + ':' + profile[trate])
                self._cursor.execute("""INSERT INTO artist_profile (artist_id, header, content) VALUES (%s,%s,%s);""",(query_data))
                self._db.commit()
            except:
                logging.error('Profile trate in db already - ' + trate)


    def store_tracks(self, tracks, artist_id):
        logging.info("DB: Stioring artist profile to db")
        for track in tracks:
            try:
                self._cursor.execute("""INSERT INTO track_list (artist_id, track_name) VALUES (%s,%s);""", (artist_id, track))
                self._db.commit()
            except:
                logging.error('Track in db already - ' + track)


    #pipline methods
    def open_spider(self, spider):
        self._connect()
        logging.info('Opened the connection to db')


    def  close_spider(self, spider):
        self._disconnect()
        logging.info('Closed the connection to db')


    def process_item(self, item, spider):
        pass
        logging.info('Connected to the db')
        logging.debug('Got the data in the pipeline')
        logging.debug(item['name'])
        logging.debug(item['profile'])
        logging.debug(item['track_list'])

        artist_id = self.store_name(item['name'])
        if artist_id is None:
            logging.error('DB ERROR: Artist already in db')
            return item

        self.store_profile(item['profile'], artist_id)
        self.store_tracks(item['track_list'], artist_id)

        self.count = self.count + 1
        logging.debug('Current count is ')
        logging.debug(self.count)
        return item
