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


@app.route('/commodity_manage/', methods=["POST", "GET"])
def commodity_manage():
    db_handler = DBManager()
    db_handler.que("Commodity", que_all=True)
    res = db_handler.get_all()
    if request.method == "GET":
        db_handler.shut()
        return render_template("commodity_manage.html", commodity=res)
    if request.form["com_name"] == "":
        search_name = request.form["search_com_name"]
        search_id = request.form["search_com_id"]
        search_cate = request.form["search_com_cate"]

    """
    name = request.form.get("com_name")
    com_id = request.form.get("com_id")
    cate = request.form.get("com_cate")
    spec = request.form.get("com_spec")
    unit = request.form.get("com_unit")
    desc = request.form.get("com_desc")
    db_handler.ins("Commodity",
                   {"field": "Name", "value": name},
                   {"field": "Id", "value": com_id},
                   {"field": "Description", "value": desc},
                   {"field": "Specifications", "value": spec},
                   {"field": "Unit", "value": unit},
                   {"field": "Category", "value": cate})
    db_handler.commit()
    """
    db_handler.shut()
    return redirect(url_for("commodity_manage", commodity=res))


@app.route('/warehouse_manage/', methods=["POST", "GET"])
def warehouse_manage():
    return render_template("warehouse_manage.html")


@app.route('/purchasing_manage/', methods=["POST", "GET"])
def purchasing_manage():
    return render_template("purchasing_manage.html")


@app.route('/refunding_manage/', methods=["POST", "GET"])
def refunding_manage():
    return render_template("refunding_manage.html")


@app.route('/view_stock/', methods=["POST", "GET"])
def view_stock():
    return render_template("view_stock.html")


@app.route('/stock_transfer/', methods=["POST", "GET"])
def stock_transfer():
    return render_template("stock_transfer.html")


@app.route('/setting/', methods=["POST", "GET"])
def setting_page():
    return render_template("setting.html")


@app.route('/logout/')
def logout():
    del session['user_info']
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
