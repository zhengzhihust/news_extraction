import sys

import pymysql

from database.dbsettings import CONFIG


class Database:
    def __init__(self):

        try:
            self.con = pymysql.connect(**CONFIG)
            self.cur = self.con.cursor()

        except pymysql.err.OperationalError:
            sys.exit("Invalid Input: Wrong username/database or password found, please try again!")

    def list_employees(self):
        self.cur.execute("SELECT * FROM sqlResult_1558435 LIMIT 50")
        result = self.cur.fetchall()
        return result
