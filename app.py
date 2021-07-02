from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/login/', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("signin.html")
    usr = request.form.get("usr")
    pwd = request.form.get("pwd")
    if usr == "123@123.com" and pwd == "123":
        session['user_info'] = usr
        return redirect('/index')
    else:
        return render_template('signin.html', msg='用户名或密码输入错误')


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
