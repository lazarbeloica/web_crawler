import MySQLdb
import logging

class DiscozDBDriver():
    db_info = {"user" : "db-psz",
                "psw" : "psz",
                "host" : "127.0.0.1",
                "db" : "discoz"
                }

    def _connect(self):
        self._db = MySQLdb.connect(host=self.db_info["host"],
                     user=self.db_info["user"],
                     passwd=self.db_info["psw"],
                     db=self.db_info["db"])

        logging.info("DB: Conecred")
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

    def store_name(self, name):
        logging.info("DB: New name stored to db")
        print (self._cursor.execute("INSERT INTO artist (name) VALUES ( " + name + " ); "))
        self._db.commit()
