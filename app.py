import os

from flask import Flask, render_template, request, redirect, session

from Util.db_manager import DB_Manager

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/login/', methods=["POST", "GET"])
def login():
    db_handler = DB_Manager()
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
    db_handler = DB_Manager()
    if request.method == "GET":
        return render_template("signup.html")
    usr = request.form.get("usr")
    pwd = request.form.get("pwd")
    if db_handler.if_in_db(usr, "Users", "Username"):
        db_handler.shut()
        return render_template('signup.html', msg='用户名已存在')
    db_handler.ins("Users", {"field": "Username", "value": usr}, {"field": "Passwd", "value": pwd})
    return render_template('signin.html', msg='创建成功')



@app.route('/index/', methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route('/commodity_manage/', methods=["POST", "GET"])
def commodity_manage():
    return render_template("commodity_manage.html")


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
