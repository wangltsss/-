import os

from flask import Flask, render_template, request, redirect, session, url_for

from Util.db_manager import DBManager

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/login/', methods=["POST", "GET"])
def login():
    db_handler = DBManager()
    if request.method == "GET":
        return render_template("signin.html")
    usr = request.form.get("usr")
    pwd = request.form.get("pwd")
    if db_handler.if_in_db(usr, "Users", "Username"):
        if db_handler.if_in_db_where(pwd, "Users", "Passwd", pair=["Username", usr]):
            session['user_info'] = usr
            db_handler.shut()
            global commodity_data
            commodity_data = "First"
            return redirect('/index')
        else:
            db_handler.shut()
            return render_template('signin.html', msg='密码输入错误')
    else:
        db_handler.shut()
        return render_template('signin.html', msg='用户名输入错误')


@app.route('/signup/', methods=["POST", "GET"])
def signup():
    db_handler = DBManager()
    if request.method == "GET":
        return render_template("signup.html")
    usr = request.form.get("usr")
    pwd = request.form.get("pwd")
    if db_handler.if_in_db(usr, "Users", "Username"):
        db_handler.shut()
        return render_template('signup.html', msg='用户名已存在')
    db_handler.ins("Users", {"field": "Username", "value": usr}, {"field": "Passwd", "value": pwd})
    db_handler.commit()
    db_handler.shut()
    return redirect(url_for('login', msg="创建成功"))


@app.route('/index/', methods=["POST", "GET"])
def index():
    return render_template("index.html")


commodity_data = "First"    # a flag that signifies the page is being opened as a new page.
@app.route('/commodity_manage/', methods=["POST", "GET"])
def commodity_manage():

    global commodity_data

    db_handler = DBManager()

    table = "Commodity"

    r_num = int(db_handler.get_last_record(table, "Id")[0][0])

    # load all records in database if this is a new page
    if commodity_data == "First":
        db_handler.que(table, que_all=True)
        commodity_data = db_handler.get_all()

    # return the webpage if the request method is "Get"
    if request.method == "GET":
        db_handler.shut()
        return render_template("commodity_manage.html", commodity=commodity_data, r_num=r_num+1)

    # get custom query conditions from search form
    search_name = request.form.get("search_com_name")
    search_id = request.form.get("search_com_id")
    search_cate = request.form.get("search_com_cate")

    # query data from database with specified conditions
    db_handler.multi_where_que(*(table,
                                 None,
                                 "Like",
                                 True,
                                 ["Name", "%{}%".format(search_name)],
                                 ["Id", "%{}%".format(search_id)],
                                 ["Category", "%{}%".format(search_cate)]))
    commodity_data = db_handler.get_all()

    # if record insertion form has contents, then implement insertion
    if request.form.get("com_name"):
        name = request.form.get("com_name")
        com_id = r_num + 1
        cate = request.form.get("com_cate")
        spec = request.form.get("com_spec")
        unit = request.form.get("com_unit")
        desc = request.form.get("com_desc")
        db_handler.ins(table,
                       {"field": "Name", "value": name},
                       {"field": "Id", "value": com_id},
                       {"field": "Description", "value": desc},
                       {"field": "Specifications", "value": spec},
                       {"field": "Unit", "value": unit},
                       {"field": "Category", "value": cate})
        db_handler.commit()
        db_handler.que(table, que_all=True)
        commodity_data = db_handler.get_all()

    # if any checkbox is checked, then implement deletion
    if request.form.getlist("s-record"):
        record_ls = request.form.getlist("s-record")
        db_handler.rmv_by_where(table, "Id", record_ls)
        db_handler.commit()
        db_handler.que(table, que_all=True)
        commodity_data = db_handler.get_all()

    # close connection to database
    db_handler.shut()
    return redirect(url_for("commodity_manage"))


@app.route('/stock_manage/', methods=["POST", "GET"])
def stock_manage():
    return render_template('stock_manage.html')


@app.route('/view_stock_in/', methods=["POST", "GET"])
def view_stock_in():
    return render_template("view_stock_in.html")


@app.route('/view_stock_out/', methods=["POST", "GET"])
def view_stock_out():
    return render_template("view_stock_out.html")


@app.route('/setting/', methods=["POST", "GET"])
def setting_page():
    return render_template("setting.html")


@app.route('/logout/')
def logout():
    del session['user_info']
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
