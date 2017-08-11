from flask import Flask, request, Response, jsonify
from flask_mysqldb import MySQL
import json
import os
import logging
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__) 


app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_DB_HOST']
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_DB_PASSWORD']
app.config['MYSQL_DB'] = 'orders'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/place-order', methods=['POST'])
def placeOrder():
    logger.info("Entered Order service to place an order")
    data = json.loads(request.data)
    try:
        logger.info("Creating MySQL cursor")
        cur = mysql.connection.cursor()
        logger.info("Executing INSERT query to insert order details")
        cur.execute("INSERT INTO orders(cart_id, order_status) VALUES({0}, '{1}')".format(data['cartId'], "Pending Payment"))
        logger.info("Executing SELECT query to obtain order ID")
        result = cur.execute("SELECT * from orders where cart_id = {}".format(data['cartId']))
        result = cur.fetchone()
        headers = {'content-type': 'application/json'} 
        data = json.dumps(data)
        url = 'http://cart:5003/change-state'
        logger.info("Making a request to Cart to change the cart state")
        response = requests.post(url, data=data, headers=headers)
        logger.debug("Response from Cart: {}".format(response.status_code))
        if response.status_code is 200:
           data = {"orderId": result['order_id']}
           mysql.connection.commit()
           cur.close()
           logger.info("Leaving Order successfully")
           return jsonify(data), 200
        else:
           logger.info("Execution Failed on Cart. Leaving Order.")
           return 500
    except:
        logger.info("Execution failed. Leaving order")
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
    logger.info("Entering Orders service to fetch order details")
    data = json.loads(request.data)
    logger.debug("Data received: {}".format(data))
    try:
        logger.info("Creating a MySQL cursor")
        cur = mysql.connection.cursor()
        orders = []
        for item in data['cartIds']:
            logger.debug("Item: {}".format(item))
            logger.info("Executing SELECT query for each cart ID")
            cur.execute("SELECT * from orders where cart_id = {}".format(item))
            result = cur.fetchone()
            orders.append(result.copy())
        logger.debug("Order details: {}".format(orders))            
        return jsonify(orders), 200
    except:
        return 500

app.run(port=5004, debug=True, host='0.0.0.0')
