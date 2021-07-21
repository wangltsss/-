import os

from flask import Flask, render_template, request

from Util.subpages import SignIn, SignUp, Index, CommodityManage, Logout, session_auth

from Util.user import User

from Exceptions import db_exceptions

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

db_mark = False
com_db = ()


@app.route('/login/', methods=["POST", "GET"])
def login():
    manager = SignIn()
    if request.method == "GET":
        return manager.build_page()
    new_session = User()
    if new_session.correct_identity():
        new_session.create_session()
        global db_mark
        global com_db
        db_mark = True
        com_db = ()
        return manager.redirect()
    else:
        return manager.build_page(err=True)


@app.route('/signup/', methods=["POST", "GET"])
def signup():
    manager = SignUp()
    if request.method == "GET":
        return manager.build_page()
    new_session = User()
    if new_session.has_duplicate():
        return manager.build_page(err=True)
    else:
        new_session.create_usr()
        return manager.build_page(suc=True)


@app.route('/index/', methods=["POST", "GET"])
@session_auth
def index():
    manager = Index()
    return manager.build_page()


@app.route('/commodity_manage/', methods=["POST", "GET"])
@session_auth
def commodity_manage():
    global db_mark

    global com_db

    manager = CommodityManage()

    [com_db, db_mark] = manager.init_db(db_mark, com_db)

    if request.form.get("search_com_name") \
            or request.form.get("search_com_id") \
            or request.form.get("search_com_cate"):
        manager.set_records(manager.search())
        com_db = manager.search()

    manager.set_records(com_db)

    try:
        if request.method == "GET":
            return manager.build_page()
    except Exception:
        return manager.to_err()

    # if record insertion form has contents, then implement insertion
    manager.insert()

    # if any checkbox is checked, then implement deletion
    manager.remove()

    # if alter form has contents, then implement alter
    manager.alter()

    return manager.redirect()


@app.route('/stock_manage/', methods=["POST", "GET"])
@session_auth
def stock_manage():
    return render_template('stock_manage.html')


@app.route('/view_stock_in/', methods=["POST", "GET"])
@session_auth
def view_stock_in():
    return render_template("view_stock_in.html")


@app.route('/view_stock_out/', methods=["POST", "GET"])
@session_auth
def view_stock_out():
    return render_template("view_stock_out.html")


@app.route('/setting/', methods=["POST", "GET"])
@session_auth
def setting_page():
    return render_template("setting.html")


@app.route('/logout/')
def logout():
    manager = Logout()
    manager.clear_session()
    return manager.redirect()


@app.route('/db-error/')
def err_page():
    return render_template("error_page.html")


if __name__ == '__main__':
    app.run(debug=True)
