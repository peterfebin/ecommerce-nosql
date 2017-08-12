from flask import Flask, request, Response, jsonify
import json
import os
import logging
import requests
import random
from pymongo import MongoClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

client = MongoClient('ordersdb', 27017)
db = client.ordersDb

@app.route('/place-order', methods=['POST'])
def placeOrder():
    logger.info("Entered Order service to place an order")
    data = json.loads(request.data)
    try:
     while True:
       try:
          logger.info("Creating new order")
          ordersId = random.randint(1, 1000)
          db.orders.insert({'_id': ordersId, 'cart_id': data['cartId'], 'order_status': 'Pending Payment'})
       except:
          continue
       break
     logger.info("Fetching order")
     order = db.orders.find_one({'cart_id': data['cartId']})
     headers = {'content-type': 'application/json'} 
     data = json.dumps(data)
     url = 'http://cart:5003/change-state'
     logger.info("Making a request to Cart to change the cart state")
     response = requests.post(url, data=data, headers=headers)
     logger.debug("Response from Cart: {}".format(response.status_code))
     if response.status_code is 200:
       logger.info("Returning order Id successfully")
       data = {"orderId": order['_id']}
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
    logger.info("Entered orders to update order status")
    data = json.loads(request.data)
    try:
        logger.info("Updating order status")
        db.orders.update({'_id': data['orderId']}, {'$set': {'order_status': 'Amount Paid'}})
        logger.info("Sunncessfully leaving Orders")
        response = Response(status=200)
    except:
        logger.info("Execution failed. Leaving Orders")
        response = Response(status=500)
    return response

@app.route('/orders', methods=['POST'])
def orders():
    logger.info("Entering Orders service to fetch order details")
    data = json.loads(request.data)
    logger.debug("Data received: {}".format(data))
    orders = []
    try:
       logger.info("Fetching all orders")
       for cartId in data['cartIds']:
          order = db.orders.find_one({'cart_id': cartId})
          orders.append(order)
       logger.info("Leaving cart successfully")
       return jsonify(orders), 200
    except:
       return 500

app.run(port=5004, debug=True, host='0.0.0.0')
