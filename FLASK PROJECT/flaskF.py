from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "rubesh"
app.config["MYSQL_DB"] = "rubesh"
app.config["MYSQL_CURSOR CLASS"] = "DictCursor"
mysql = MySQL(app)


@app.route("/")
def home():
    return render_template('/home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        if username == 'rubesh@123' and password == '123':
            session['username'] = username
            return redirect('/company')
        else:
            return 'Login failed. Please try again.'
    username = request.form['name']
    password = request.form['password']
    if username == 'rubesh@123' and password == '123':
        session['username'] = username
        return redirect('/company')
    else:
        return 'Login failed. Please try again.'


@app.route("/addItems")
def addItems():
    con = mysql.connection.cursor()
    sql = "select * from items"
    con.execute(sql)
    res = con.fetchall()
    return render_template("addItems.html", datas=res)


@app.route("/addItem", methods=['POST', 'GET'])
def addItem():
    con = mysql.connection.cursor()
    if request.method == 'POST':
        id1 = request.form.get('id1')
        name1 = request.form.get('iName')
        qty1 = request.form.get('qty')
        rte1 = request.form.get('rte')
        sql = ("insert into items(item_id, item_name, quantity, rate, amount) values(%d,'%s',%d,%d,%d * %d) on "
               "duplicate key update items.quantity= items.quantity + %d, items.amount= items.amount + (%d * %d)")
        con.execute(sql % (int(id1), name1, int(qty1), int(rte1), int(rte1), int(qty1), int(qty1), int(qty1), int(rte1)))
        mysql.connection.commit()
        con.close()
        return redirect('/addItems')
    id1 = request.form.get('id1')
    name1 = request.form.get('iName')
    qty1 = request.form.get('qty')
    rte1 = request.form.get('rte')
    sql = ("insert into items(item_id, item_name, quantity, rate, amount) values(%d,'%s',%d,%d,%d * %d) on "
           "duplicate key update items.quantity= items.quantity + %d, items.amount= items.amount + (%d * %d)")
    con.execute(sql % (int(id1), name1, int(qty1), int(rte1), int(rte1), int(qty1), int(qty1), int(qty1), int(rte1)))
    mysql.connection.commit()
    con.close()
    return redirect('/addItems')


@app.route("/addExtraItems", methods=['GET', 'POST'])
def addExtraItems():
    if request.method == 'POST':
        return render_template('addExtraItems.html')
    else:
        return render_template('addExtraItems.html')


@app.route("/updatePurchaseItems/<string:id>/<int:qty>/<int:amount>", methods=['GET', 'POST'])
def updatePurchaseItems(id, qty, amount):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        val = "insert into purchase select * from items where items_id=%s"
        con.execute(val % int(id))
        mysql.connection.commit()
        sql = ("insert into purchase_items select * from items where item_id=%s on duplicate key update "
               "purchase_items.quantity ="
               "purchase_items.quantity + %d, purchase_items.amount= purchase_items.amount + purchase_items.rate * %d")
        con.execute(sql % (id, int(qty), int(qty)))
        mysql.connection.commit()
        con.execute("select * from company");
        ls = con.fetchall()
        total_amount = (ls[0][-1])
        total_amount -= int(amount);
        if total_amount<0:
            return "<center><h1>YOU HAVE NOT ENOUGH MONEY</h1></center>"
        casB = "update company set cash_balance = %d where company_id=1001"
        con.execute(casB % (int(total_amount)))
        mysql.connection.commit()
        con.close()
        return redirect('/purchased_items')
    val = "insert into purchase select * from items where item_id=%s"
    con.execute(val % int(id))
    mysql.connection.commit()
    sql = ("insert into purchase_items select * from items where item_id=%s on duplicate key update "
           "purchase_items.quantity ="
           "purchase_items.quantity + %d, purchase_items.amount= purchase_items.amount + purchase_items.rate * %d")
    con.execute(sql % (id, int(qty), int(qty)))
    mysql.connection.commit()
    con.execute("select * from company");
    ls = con.fetchall()
    total_amount = (ls[0][-1])
    total_amount -= int(amount);
    if total_amount < 0:
        return "<h1>YOU HAVE NOT ENOUGH MONEY</h1>"
    casB = "update company set cash_balance = %d where company_id=1001"
    con.execute(casB % (int(total_amount)))
    mysql.connection.commit()
    con.close()
    return redirect('/purchased_items')


@app.route("/upAddItems", methods=['POST', 'GET'])
def upAddItems():
    if request.method == 'POST':
        con = mysql.connection.cursor()
        id1 = request.form.get('id1')
        name = request.form.get('name')
        qty = request.form.get('qty')
        rate = request.form.get('rate')
        sql = "update items set item_name='%s', quantity=%d, rate=%d, amount=%d * %d where item_id='%s'" % (
            str(name), int(qty), int(rate), int(rate), int(qty), str(id1))
        con.execute(sql)
        mysql.connection.commit()
        con.close()
        return redirect('addItems')
    con = mysql.connection.cursor()
    id1 = request.form.get('id1')
    name = request.form.get('name')
    qty = request.form.get('qty')
    rate = request.form.get('rate')
    sql = "update items set item_name='%s', quantity=%d, rate=%d, amount=%d * %d where item_id='%s'" % (
        str(name), int(qty), int(rate), int(rate), int(qty), str(id1))
    con.execute(sql)
    mysql.connection.commit()
    con.close()
    return redirect('/addItems')


@app.route("/editAvailableItems/<string:id>", methods=['GET', 'POST'])
def editAvailableItems(id):
    if request.method == 'POST':
        con = mysql.connection.cursor()
        sql = "select * from items where item_id=%d" % int(id)
        con.execute(sql)
        res = con.fetchall()
        con.close()
        return render_template('editNewItem.html', datas=res)
    con = mysql.connection.cursor()
    sql = "select * from items where item_id=%d"
    con.execute(sql % int(id))
    res = con.fetchall()
    con.close()
    return render_template('editNewItem.html', datas=res)


@app.route("/company", methods=['POST', 'GET'])
def company():
    if request.method == 'POST':
        con = mysql.connection.cursor()
        sql = "select * from company"
        con.execute(sql)
        res = con.fetchall()
        return render_template('companies.html', row=res)
    else:
        con = mysql.connection.cursor()
        sql = "select * from company"
        con.execute(sql)
        res = con.fetchall()
        return render_template('companies.html', row=res)


@app.route("/purchased_items", methods=['GET', 'POST'])
def purchased_items():
    if request.method == 'POST':
        con = mysql.connection.cursor()
        sql = "select * from company where company_id=1001"
        con.execute(sql)
        cB = con.fetchall()[0][-1]
        print(cB)
        con = mysql.connection.cursor()
        sql = "select * from purchase_items"
        con.execute(sql)
        res = con.fetchall()
        return render_template('purchasedItems.html', datas=res, cB=cB)
    else:
        con = mysql.connection.cursor()
        sql = "select * from company where company_id=1001"
        con.execute(sql)
        cB = con.fetchall()[0][-1]
        con = mysql.connection.cursor()
        sql = "select * from purchase_items"
        con.execute(sql)
        res = con.fetchall()
        return render_template('purchasedItems.html', datas=res, cB=cB)


@app.route("/cal_amt/", methods=['GET', 'POST'])
def cal_amt():
    if request.method == 'POST':
        id2 = request.form.get('id1')
        rate = int(request.form.get('rate'))
        quantity = int(request.form.get('quantity'))
        amount = rate * quantity
        con = mysql.connection.cursor()
        sql = "update purchase_items set amount=%d, rate=%d where purchase_id=%s"
        con.execute(sql % (amount, rate, id2))
        mysql.connection.commit()
        con.close()
        return redirect(url_for('purchased_items'))
    id2 = request.form.get('id1')
    rate = int(request.form.get('rate'))
    quantity = int(request.form.get('quantity'))
    amount = rate * quantity
    con = mysql.connection.cursor()
    sql = "update purchase_items set amount={}, rate={} where purchase_id=%s".format(amount, rate, id2)
    con.execute(sql)
    mysql.connection.commit()
    con.close()
    return redirect(url_for('purchased_items'))


@app.route("/saleItem", methods=['GET', 'POST'])
def saleItem():
    if request.method == 'POST':
        con = mysql.connection.cursor()
        sql = "select * from company where company_id=1001"
        con.execute(sql)
        cB = con.fetchall()[0][-1]
        con = mysql.connection.cursor()
        sql = "select * from sales_items"
        con.execute(sql)
        res = con.fetchall()
        return render_template('salesItems.html', datas=res, cB=cB)
    else:
        con = mysql.connection.cursor()
        sql = "select * from company where company_id=1001"
        con.execute(sql)
        cB = con.fetchall()[0][-1]
        con = mysql.connection.cursor()
        sql = "select * from sales_items"
        con.execute(sql)
        res = con.fetchall()
        return render_template('salesItems.html', datas=res, cB=cB)


@app.route("/showItems")
def showItems():
    con = mysql.connection.cursor()
    sql2 = "select * from sales_items"
    con.execute(sql2)
    res = con.fetchall()
    con.close()
    return render_template('salesItems.html', datas=res)


@app.route("/upQtySaleItems/<int:id>/<string:name>/<int:qty>/<int:rate>/<string:amount>", methods=['POST', 'GET'])
def upQtySaleItems(id, name, qty, rate, amount):
    if request.method == 'POST':
        if int(qty) == 0 :
            return "<center><h1>YOUR ITEM IS NOT ENOUGH</h1></center>"
        return render_template("/chgeQtySale.html", id=id, name=name, qty=qty, rate=rate, amount=amount)
    else:
        if int(qty) == 0 :
            return "<center><h1>YOUR ITEM IS NOT ENOUGH</h1></center>"
        return render_template("/chgeQtySale.html", id=id, name=name, qty=qty, rate=rate, amount=amount)


@app.route("/saleOp", methods=['GET', 'POST'])
def saleOp():
    print("ruby")
    con = mysql.connection.cursor()
    if request.method == 'POST':
        id1 = request.form.get('id')
        name1 = request.form.get('name')
        qty1 = request.form.get('qty')
        rate1 = request.form.get('rate')
        amount1 = request.form.get('amount')
        print(qty1)
        val = "select * from purchase_items where purchase_id = %d"
        con.execute(val % int(id1))
        ls = con.fetchall()
        total_amount = (ls[0][-3])
        print(total_amount)
        if int(qty1) > total_amount or (int(qty1) <= 0):
            con.execute("select * from company")
            ls = con.fetchall()
            total_amount = (ls[0][-1])
            total_amount += int(amount1)
            casB = "update company set cash_balance = (cash_balance+%d) where company_id=1001"
            con.execute(casB % (int(total_amount)))
            mysql.connection.commit()
            con.close()
            return redirect("/showItems")
        else:
            val = ("update purchase_items set purchase_items.quantity = (purchase_items.quantity - %d) where "
                   "purchase_id=%d")
            con.execute(val % (int(qty1), int(id1)))
            mysql.connection.commit()
            sql = ("insert into sales_items(sales_id, sales_name, quantity, rate, amount) values('%s', '%s', %d, %d, "
                   "%d) on duplicate key update sales_items.quantity =  sales_items.quantity + %d, sales_items.rate = "
                   "sales_items.rate +%d, sales_items.amount =  sales_items.amount + (%d * %d)")
            con.execute(
                sql % (id1, name1, int(qty1), int(rate1), int(amount1), int(qty1), int(rate1), int(rate1), int(qty1)))
            mysql.connection.commit()
            con.execute("select * from company")
            ls = con.fetchall()
            total_amount = (ls[0][-1])
            total_amount += int(amount1)
            casB = "update company set cash_balance = (cash_balance+%d) where company_id=1001"
            con.execute(casB % (int(total_amount)))
            mysql.connection.commit()
            con.close()
            return redirect("/showItems")
    id1 = request.form.get('id')
    name1 = request.form.get('name')
    qty1 = request.form.get('qty')
    rate1 = request.form.get('rate')
    amount1 = request.form.get('amount')
    print(qty1)
    val = "select * from purchase_items where purchase_id = %d"
    con.execute(val % int(id1))
    ls = con.fetchall()
    total_amount = (ls[0][-3])
    print(total_amount)
    if int(qty1) > total_amount or (int(qty1) <= 0):
        con.execute("select * from company")
        ls = con.fetchall()
        total_amount = (ls[0][-1])
        total_amount += int(amount1)
        casB = "update company set cash_balance = %d where company_id=1001"
        con.execute(casB % total_amount)
        mysql.connection.commit()
        con.close()
        return redirect("/showItems")
    else:
        val = ("update purchase_items set purchase_items.quantity = (purchase_items.quantity - %d) where "
               "purchase_id=%d")
        con.execute(val % (int(qty1), int(id1)))
        mysql.connection.commit()
        sql = ("insert into sales_items(sales_id, sales_name, quantity, rate, amount) values('%s', '%s', %d, %d, "
               "%d) on duplicate key update sales_items.quantity =  sales_items.quantity + %d, sales_items.rate = "
               "sales_items.rate +%d, sales_items.amount =  sales_items.amount + (%d * %d)")
        con.execute(
            sql % (id1, name1, int(qty1), int(rate1), int(amount1), int(qty1), int(rate1), int(rate1), int(qty1)))
        mysql.connection.commit()
        con.execute("select * from company")
        ls = con.fetchall()
        total_amount = (ls[0][-1])
        total_amount += int(amount1)
        casB = "update company set cash_balance = %d where company_id=1001"
        con.execute(casB % total_amount)
        mysql.connection.commit()
        con.close()
        return redirect("/showItems")


@app.route("/purchase", methods=['POST', 'GET'])
def purchase():
    con = mysql.connection.cursor()
    sql = "select * from company where company_id=1001"
    con.execute(sql)
    cB=con.fetchall()[0][-1]
    con = mysql.connection.cursor()
    sql = "select * from purchase"
    con.execute(sql)
    res = con.fetchall()
    con.close();
    return render_template("purchase.html", datas=res, cB=cB)


@app.route("/viewUser/<int:id>", methods=['GET', 'POST'])
def viewUser(id):
    if request.method == 'POST':
        con = mysql.connection.cursor()
        sql = "select * from company where company_id=%d"
        con.execute(sql % int(id))
        res = con.fetchone()
        return render_template('companyD.html', datas=res)
    con = mysql.connection.cursor()
    val = "select * from company where company_id=%d"
    con.execute(val % int(id))
    res = con.fetchone()
    return render_template('companyD.html', datas=res)


@app.route("/editPrice/<string:id>", methods=['GET', 'POST'])
def editPrice(id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        id1 = request.form.get(id)
        sql = "select * from purchase_items where purchase_id=%s"
        con.execute(sql % id)
        res = con.fetchall()
        return render_template('editPrice.html', datas=res, id=id1)
    sql = "select * from purchase_items where purchase_id=%s"
    con.execute(sql % id)
    res = con.fetchall()
    return render_template('editPrice.html', datas=res, id1=id)


@app.route("/verify", methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        return render_template('loginPage.html')
    else:
        return render_template('loginPage.html')


if __name__ == '__main__':
    app.run(debug=True)
