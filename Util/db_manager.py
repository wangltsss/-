from Util.db_parser import DBParser


db_conf = "conf/sql_conf.json"


class DBManager(DBParser):

    def __init__(self):
        self.connect_db(db_conf)
        self.create_cursor()

    def commit(self):
        self.conn.commit()

    def get_all(self):
        return self.db_cursor.fetchall()

    def get_one(self):
        return self.db_cursor.fetchone()

    def get_many(self, size):
        return self.db_cursor.fetchmany(size)

    def que(self, table, *cond, que_all=False):
        if que_all:
            self.execute("SELECT * FROM " + table)
        else:
            res = ''
            for i in cond:
                res += str(i[0]) + ", "
            res = res.rstrip()
            res = res.rstrip(",")
            self.execute("SELECT " + res + " FROM " + table)

    def where_affix_que(self, table, *col, que_all=False, pair, mode="LIKE"):
        if que_all:
            self.execute("SELECT * FROM " + table + " WHERE {} {} {}".format(pair[0], mode, "'" + pair[1] + "'"))
        else:
            res = ''
            for i in col:
                res += str(i[0]) + ", "
            res = res.rstrip()
            res = res.rstrip(",")
            self.execute(
                "SELECT " + res + " FROM " + table + " WHERE {} {} {}".format(pair[0], mode, "'" + pair[1] + "'"))

    def multi_where_que(self, table, col, que_all=False, mode="Like", *pair):
        cond = ""
        for i in pair:
            cond += i[0] + mode + "'" + i[1] + "' AND"
        cond = cond.strip("' AND")
        if que_all:
            self.execute("SELECT * FROM " + table + " WHERE {}".format(cond))
        else:
            self.execute("SELECT " + col + "  FROM " + table + " WHERE {}".format(cond))

    def ins(self, table, *pairs,):
        if len(pairs) == 0:
            return
        fields = ''
        values = ''
        for i in pairs:
            fields += str(i["field"]) + ", "
            values += "'{}', ".format(i["value"])
        fields = fields.rstrip()
        fields = fields.rstrip(",")
        values = values.rstrip()
        values = values.rstrip(",")
        self.execute("INSERT INTO {} ({}) VALUES({})".format(table, fields, values))
        #new.ins("Users", {"field": "Username", "value": "12@12.com"}, {"field": "Passwd", "value": "12"})

    def drop(self, table):
        pass

    def alt(self, table):
        pass

    def shut(self):
        self.disconnect_db()

    def if_in_db(self, record, table, *column):
        if len(column):
            self.que(table, column)
        else:
            self.que(table, que_all=True)
        res = self.db_cursor.fetchall()
        for i in res:
            if record in i:
                return True
            else:
                pass
        return False

    def if_in_db_where(self, record, table, *column, pair, mode="LIKE"):
        if len(column):
            self.where_affix_que(table, column, pair=pair, mode=mode)
        else:
            self.where_affix_que(table, que_all=True, pair=pair, mode=mode)
        res = self.db_cursor.fetchall()
        for i in res:
            if record in i:
                return True
            else:
                pass
        return False



new = DBManager()
new.que("Commodity", que_all=True)
res = new.db_cursor.fetchall()
print(res)


