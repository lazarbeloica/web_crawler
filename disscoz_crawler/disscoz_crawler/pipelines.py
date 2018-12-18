# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import MySQLdb
from dateutil import parser


class DisscozCrawlerDBPipeline(object):

    db_info = {"user" : "scrapy",
            "psw" : "passwrd",
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


    def get_artist_id(self, name):
        try:

            self._cursor.execute("""select id from artist where artist_name="%s"; """, (name,))
            self._db.commit()

            artist_id = self._cursor.fetchone()

            return artist_id
        except Exception as err:
            self._db.rollback()
            logging.error(err)
            logging.error('Something Wrong with getting id for - ' + name)
            raise Exception("Couldn't get artist id")


    def store_artist_name(self, name):
        try:

            logging.debug('DB: Storing name ' + name)
            self._cursor.execute("""INSERT INTO artist (artist_name) VALUES (%s); """, (name,))
            self._db.commit()

            artist_id = self._cursor.lastrowid
            logging.debug(artist_id)
            return artist_id
        except Exception as err:
            self._db.rollback()
            logging.error(err)
            logging.error('Artist already in db - ' + name)
            raise Exception("Artist is in db already" + name)


    def convert_to_date(self, date_str):
        dt = parser.parse(date_str)
        logging.debug(dt)
        return dt


    def store_general_album_info(self, album_name, vesions, released, country, artist_id):
        try:
            logging.debug('DB: Storing album name ' + album_name)

            if released:
                query_data = [artist_id, album_name, vesions, self.convert_to_date(released), country]
                self._cursor.execute("""INSERT INTO album (artist_id, album_name, versions, released, country ) VALUES ({0},"{1}",{2},"{3}","{4}");""".format(*query_data))

            else:
                query_data = [artist_id, album_name, vesions, country]
                self._cursor.execute("""INSERT INTO album (artist_id, album_name, versions, country ) VALUES ({0},"{1}",{2},"{3}"); """.format(*query_data))

            self._db.commit()

            album_id = self._cursor.lastrowid
            logging.debug(album_id)
            return album_id

        except Exception as err:
            self._db.rollback()
            logging.error(err)
            logging.error('Album already in db - ' + album_name)
            raise Exception("Album already in db - " + album_name)


    def store_profile(self, profile, album_id):
        logging.info("DB: Stioring artalbumist profile to db")
        for trate in profile:
            try:
                if trate == 'Format':
                    formats = profile[trate].split(',')
                    for album_format in formats:

                        logging.debug('DB: Storing format:' + album_format)
                        self._cursor.execute("""INSERT INTO album_format (album_id, album_format) VALUES ({0},"{1}");""".format(album_id, album_format))
                        self._db.commit()
                        continue

                if trate == 'Style':
                    styles = profile[trate].split(',')
                    for style in styles:

                        logging.debug('DB: Storing format:' + style)
                        self._cursor.execute("""INSERT INTO album_style (album_id, style) VALUES ({0},"{1}");""".format(album_id, style))
                        self._db.commit()
                        continue

                if trate == 'Genre':
                    genres = profile[trate].split(',')
                    for genre in genres:

                        logging.debug('DB: Storing format:' + genre)
                        self._cursor.execute("""INSERT INTO album_genre (album_id, genre) VALUES ({0},"{1}");""".format(album_id, genre))
                        self._db.commit()
                        continue

                if trate != 'Release' and trate != 'Country':
                    query_data = [album_id, trate, profile[trate]]
                    logging.debug('DB: Storing trate ' + trate + ':' + profile[trate])
                    self._cursor.execute("""INSERT INTO album_misc_content (album_id, header, content) VALUES ({0},"{1}","{2}");""".format(*query_data))

            except Exception as err:
                self._db.rollback()
                logging.error(err)
                logging.error('Profile trate in db already - ' + trate + ' id is %d' % (album_id,))


    def store_tracks(self, tracks, album_id):
        logging.info("DB: Storing tracks to db")
        for track in tracks:
            try:
                self._cursor.execute("""INSERT INTO track_list (album_id, track_name) VALUES (%s,%s);""", (album_id, track))
                self._db.commit()
            except Exception as err:
                self._db.rollback()
                logging.error(err)
                logging.error('Track in db already - ' + track)


    #pipline methods
    def open_spider(self, spider):
        self._connect()
        logging.info('Opened the connection to db')


    def  close_spider(self, spider):
        self._disconnect()
        logging.info('Closed the connection to db')


    def process_item(self, item, spider):
        logging.info('Connected to the db')
        logging.debug('Got the data in the pipeline')

        try:
            artist_id = self.get_artist_id(item['artist_name'])

            if artist_id is None:
                artist_id = self.store_artist_name(item['artist_name'])
            album_id = self.store_general_album_info(item['album_name'], item['album_version'], item['profile']['Released'], item['profile']['Country'], artist_id)

            self.store_profile(item['profile'], album_id)
            self.store_tracks(item['track_list'], album_id)
        except Exception as error:
            logging.error("An error with db occured")
            logging.error(error)
            return item

        self.count = self.count + 1
        logging.debug("Current count is %d" % self.count)
        return item
