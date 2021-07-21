from Util.db_parser import DBParser


db_conf = "conf/sql_conf.json"


class DBManager(DBParser):

    def __init__(self):
        self.connect_db(db_conf)
        self.create_cursor()

    def _commit(self):
        self.conn.commit()

    def _get_all(self):
        return self.db_cursor.fetchall()

    def _get_one(self):
        return self.db_cursor.fetchone()

    def _get_many(self, size):
        return self.db_cursor.fetchmany(size)

    def _que(self, table, *cond, que_all=False):
        if que_all:
            self.execute("SELECT * FROM " + table)
        else:
            res = ''
            for i in cond:
                res += str(i[0]) + ", "
            res = res.rstrip()
            res = res.rstrip(",")
            self.execute("SELECT " + res + " FROM " + table)

    def _where_affix_que(self, table, *col, que_all=False, pair, mode="LIKE"):
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

    def _multi_where_que(self, table, col, mode="Like", que_all=False, *pair):
        cond = ""
        for i in pair:
            if i[1] is None or i[1] == '' or i[1] == '%None%':
                pass
            else:
                cond += "{} {} '{}' AND ".format(i[0], mode, i[1])
        cond = cond.rstrip(" AND ")
        if cond == "":
            self._que(table, que_all=que_all)
        else:
            if que_all:
                self.execute("SELECT * FROM " + table + " WHERE {}".format(cond))
            else:
                self.execute("SELECT " + col + "  FROM " + table + " WHERE {}".format(cond))

    def _ins(self, table, *pairs):
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

    def _rmv_by_where(self, table, col, *cond):
        clause = ""
        for i in cond:
            if not i[0] or i[0] == '':
                pass
            else:
                clause += "{}='{}' OR ".format(col, i[0])
        clause = clause.rstrip(" OR ")
        if clause == "":
            return
        self.execute("DELETE FROM {} WHERE {}".format(table, clause))

    def _alt(self, table, com_id, *pairs):
        if len(pairs) == 0:
            return
        alt_items = ""
        for i in pairs:
            alt_items += "{}='{}', ".format(i["field"], i["value"])
        alt_items = alt_items.rstrip(", ")
        self.execute("UPDATE {} SET {} WHERE Id={}".format(table, alt_items, com_id))

    def shut(self):
        self.disconnect_db()

    def _if_in_db(self, record, table, *column):
        if len(column):
            self._que(table, column)
        else:
            self._que(table, que_all=True)
        res = self.db_cursor.fetchall()
        for i in res:
            if record in i:
                return True
            else:
                pass
        return False

    def _if_in_db_where(self, record, table, *column, pair, mode="LIKE"):
        if len(column):
            self._where_affix_que(table, column, pair=pair, mode=mode)
        else:
            self._where_affix_que(table, que_all=True, pair=pair, mode=mode)
        res = self.db_cursor.fetchall()
        for i in res:
            if record in i:
                return True
            else:
                pass
        return False

    def _records_num(self, table):
        self._que(table, que_all=True)
        return len(self._get_all())

    def _get_last_record(self, table, order_by):
        self.execute("SELECT * FROM {} ORDER BY {} DESC LIMIT 1".format(table, order_by))
        return self._get_all()

    def _get_first_record(self, table, order_by):
        self.execute("SELECT * FROM {} ORDER BY {} ASC LIMIT 1".format(table, order_by))
        return self._get_all()





