from flask import Flask, request, Response, jsonify
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'orders'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/place-order', methods=['POST'])
def placeOrder():
    data = json.loads(request.data)
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders(cart_id, total_price, order_status) VALUES({0}, {1}, '{2}')".format(data['cartId'], data['totalPrice'], "Pending Payment"))
        result = cur.execute("SELECT * from orders where cart_id = {}".format(data['cartId']))
        result = cur.fetchone()
        data = {"orderId": result['order_id']}
        mysql.connection.commit()
        cur.close()
        return jsonify(data), 200
    except:
        response = Response(status=500)
    return response

@app.route('/update-order-status', methods=['POST'])
def updateOrderStatus():
    data = json.loads(request.data)
    print('DATA: ', data)
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE orders SET order_status = '{0}' WHERE order_id = {1}".format("Amount Paid", data['orderId']))
        mysql.connection.commit()
        cur.close()
        response = Response(status=200)
    except:
        response = Response(status=500)
    return response

@app.route('/orders', methods=['POST'])
def orders():
    data = json.loads(request.data)
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from orders where cart_id = {}".format(data['cartId']))
        result = cur.fetchall()
        return jsonify(result), 200
    except:
        return 500

app.run(port=5004, debug=True)
