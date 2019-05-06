import pymysql

CONFIG = {
    'host': 'cdb-q1mnsxjb.gz.tencentcdb.com',
    'port': 10102,
    'user': 'root',
    'passwd': 'A1@2019@me',
    'charset': 'utf8',
    'database': "news_chinese",
    'cursorclass': pymysql.cursors.DictCursor
}
