from Util.json_parser import Parser
import pymysql
from Exceptions.db_exceptions import *


class DB_Parser(object):
    json_parser = Parser()
    conn_flag = False
    conn = None
    db_cursor = None

    def connect_db(self, conf):
        res = self.json_parser.json_reader(conf)
        self.conn = pymysql.connect(
            host=res["ip"], user=res["username"], password=res["passwd"], db=res["db_name"], charset='utf8')
        self.conn_flag = True

    def disconnect_db(self):
        if self.conn_flag:
            self.db_cursor.close()
            self.conn.close()
        else:
            print("No connection to close!")
            raise AllConnDead

    def create_cursor(self):
        self.db_cursor = self.conn.cursor()

    def execute(self, qry):
        self.db_cursor.execute(qry)




