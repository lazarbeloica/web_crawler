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

    def _disconnect(self):
        self._db.close()

    def __init__(self):
        self._connect()

    def store_name(self, name):
        logging.info("DB: New name stored to db")
        print (self._cursor.execute("INSERT INTO artist (name) VALUES (\"" + name + "\"); "))
        self._db.commit()


