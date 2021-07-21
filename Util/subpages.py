from Util.db_manager import DBManager

from flask import Flask, render_template, request, redirect, session, url_for

from functools import wraps


class SubPage(DBManager):
    """
    子页面对象的模版
    """

    table: str
    _records: list

    def __init__(self):
        super().__init__()

    def build_page(self):
        """
        :return: 模版文件
        """
        pass

    def redirect(self):
        """
        :return: 重定向到模版文件
        """
        pass

    def get_records(self):
        return self._records

    def set_records(self, record):
        self._records = record

    def to_err(self):
        return redirect(url_for('err_page'))


class SignIn(SubPage):

    def __init__(self):
        super().__init__()
        self.table = "Users"

    def build_page(self, err=False):
        if err:
            return render_template("signin.html", msg="用户名或密码错误！")
        else:
            return render_template("signin.html")

    def redirect(self):
        self.shut()
        return redirect("/index")


class SignUp(SubPage):

    def __init__(self):
        super().__init__()
        self.table = "Users"

    def build_page(self, err=False, suc=False):
        if err:
            return render_template("signup.html", msg="用户名已经存在！")
        if suc:
            return render_template("signup.html", msg="创建成功")
        return render_template("signup.html")

    def redirect(self):
        self.shut()
        return redirect(url_for('login', msg="创建成功！"))


class Index(SubPage):

    def build_page(self):
        return render_template("index.html")


class CommodityManage(SubPage):

    _records: list
    table: str

    def __init__(self):
        super().__init__()
        self.table = "Commodity"

    def init_db(self, mark, db):
        if mark:
            db = self.search(cond=False)
        return [db, False]

    def get_records_num(self):
        return int(self._get_last_record(self.table, "ID")[0][0])

    def get_records(self):
        return self._records

    def set_records(self, records):
        self._records = records

    def build_page(self):
        return render_template("commodity_manage.html",
                               commodity=self.get_records(),
                               r_num=self.get_records_num()+1)

    def redirect(self):
        self.shut()
        return redirect(url_for("commodity_manage"))

    def search(self, cond=True):
        if not cond or request.form.get("search_com_name") == "ALL":
            self._que(self.table, que_all=True)
        elif request.form.get("search_com_name") \
                or request.form.get("search_com_id") \
                or request.form.get("search_com_cate"):
            self._multi_where_que(*(self.table,
                                    None,
                                    "Like",
                                    True,
                                    ["Name", "%{}%".format(request.form.get("search_com_name"))],
                                    ["Id", "%{}%".format(request.form.get("search_com_id"))],
                                    ["Category", "%{}%".format(request.form.get("search_com_cate"))]))
        else:
            return ()
        return self._get_all()

    def insert(self):
        if request.form.get("com_name"):
            self._ins(self.table,
                      {"field": "Name", "value": request.form.get("com_name")},
                      {"field": "Id", "value": self.get_records_num()+1},
                      {"field": "Description", "value": request.form.get("com_desc")},
                      {"field": "Specifications", "value": request.form.get("com_spec")},
                      {"field": "Unit", "value": request.form.get("com_unit")},
                      {"field": "Category", "value": request.form.get("com_cate")})
            self._commit()
            self.set_records(self.search(cond=False))

    def remove(self):
        if request.form.getlist("s-record"):
            self._rmv_by_where(self.table, "Id", request.form.getlist("s-record"))
            self._commit()
            self.set_records(self.search(cond=False))

    def alter(self):
        if request.form.get("alt_com_name"):
            self._alt(self.table,
                      request.form.get("alt_com_id"),
                      {"field": "Name", "value": request.form.get("alt_com_name")},
                      {"field": "Description", "value": request.form.get("alt_com_desc")},
                      {"field": "Specifications", "value": request.form.get("alt_com_spec")},
                      {"field": "Unit", "value": request.form.get("alt_com_unit")},
                      {"field": "Category", "value": request.form.get("alt_com_cate")})
            self._commit()
            self.set_records(self.search(cond=False))


class Logout(SignIn):

    def clear_session(self):
        session.clear()

    def redirect(self):
        return redirect('/login')


def session_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        usr = session.get('usr_info')
        if not usr:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated
























