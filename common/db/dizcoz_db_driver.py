import MySQLdb
import logging

class DiscozDBDriver():
    db_info = {"user" : "scrapy",
                "psw" : "passwrd",
                "host" : "127.0.0.1",
                "db" : "discoz"
                }

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


    def __enter__(self):
        self._connect()
        return self


    def __exit__(self,exc_type, exc_value, traceback):
        self._disconnect()


    def custom_query(self, query):
        '''
        Brief: Sends a custom query to the db

        Param [in]: query as string

        Returns: True if successfull
        '''
        self._custom_query_res = self._cursor.execute(query)


    def get_custom_query(self):
        '''
        Brief: Returns the result of the custom query if available

        Returns [in]: Query result
        '''
        return self._cursor.fetchall()
