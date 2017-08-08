from flask import Flask, Response, jsonify, request
from flask_mysqldb import MySQL
import os
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_DB_HOST']
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_DB_PASSWORD']
app.config['MYSQL_DB'] = 'catalogue'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=['POST'])
def catalogue():
    logger.info('Entered Catalogue service to list the products')
    try:
        logger.info('Creating MySQL cursor')
        cur = mysql.connection.cursor()
        logger.info("Executing SELECT query on product")
        result = cur.execute("SELECT * from product")
        logging.info("Fetchning all products")
        products = cur.fetchall()
        # productDetailsDictionary = {}
        # productDetails = []
        # # ToDo: Fix error at append
        # for product in products:
        #     location = product['location']
        #     productId = product['product_id']
        #     productDetailsDictionary['productId'] = productId
        #     productDetailsDictionary['location'] = location
        #     productDetails.append(productDetailsDictionary)
            #productDetails.append(productId, productLocation)
        #print(productDetails)
        #response = Response(status=200, response=jsonify(productDetails))
        logger.info("Leaving Catalogue service successfully")
        return jsonify({'productDetails': products}), 200
    except:
        logger.warning("Failed to execute query. Leaving Catalogue service")
        response = Response(status=500)

    return response

@app.route('/price', methods=['POST'])
def price():
   logger.info("Entered the Catalogue service to fetch price of products")
   data = json.loads(request.data)
   try:
      logger.info("Creating MySQL cursor")
      cur = mysql.connection.cursor()
      logger.info("Executing SELECT query on product to fetch details of product")
      result = cur.execute("SELECT price FROM product where product_id = {}".format(data['productId']))
      logger.info("Fetching product from cursor")
      price = cur.fetchone()
      logger.info("Fetching product price")
      price = price['price']
      data = {"price": price}
      return jsonify(data), 200
   except:
      logger.warning("Execution failed. Leaving Catalogue")
      response.status = 500
      return response


app.run(port=5001, debug=True, host='0.0.0.0')
