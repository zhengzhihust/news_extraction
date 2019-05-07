import sys

import pymysql

from database.dbsettings import CONFIG, SELECT_SQL, SELECT_ALL


class Database:
    def __init__(self):

        try:
            self.con = pymysql.connect(**CONFIG)
            self.cur = self.con.cursor()

        except pymysql.err.OperationalError:
            sys.exit("Invalid Input: Wrong username/database or password found, please try again!")

    def list_data(self):
        self.cur.execute(SELECT_SQL)
        result = self.cur.fetchall()
        return result

    def list_all_data(self):
        self.cur.execute(SELECT_ALL)
        result = self.cur.fetchall()
        return result
