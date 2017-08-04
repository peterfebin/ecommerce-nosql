from flask import Flask, Response, jsonify
from flask_mysqldb import MySQL
import os
import logging

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_DB_HOST']
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_DB_PASSWORD']
app.config['MYSQL_DB'] = 'catalogue'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=['POST'])
def catalogue():
    print("HIT")
    logging.warning('ENTERED CATALOGUE')
    cur = mysql.connection.cursor()
    logging.warning('CREATED CURSOR')
    try:
        result = cur.execute("SELECT * from product")
        logging.warning("EXECUTED SELECT QUERY")
        products = cur.fetchall()
        logging.warning("FETCHED ALL PRODUCTS")
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
        return jsonify({'productDetails': products}), 200
    except:
        logging.warning("FAILED")
        response = Response(status=500)

    return response


app.run(port=5001, debug=True, host='0.0.0.0')
