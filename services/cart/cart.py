from flask import Flask, request, Response, jsonify
from flask_mysqldb import MySQL
import json
import requests
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_DB_HOST']
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_DB_PASSWORD']
app.config['MYSQL_DB'] = 'cart'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/add-to-cart', methods=['POST'])
def addToCart():
    logger.info("Entered Cart service to add a product to cart")
    data = json.loads(request.data)
    try:
        logger.info("Creating a MySQL cursor")
        cur = mysql.connection.cursor()
        logger.info("Executing SELECT query on cart table to check if a cart already exists")
        result = cur.execute("SELECT * FROM cart where user_id = {} and state = '{}'".format(data['userId'], 'ACTIVE'))
        if result == 0:
            logger.info("Executing INSERT query on cart table to create a new cart for the logged in user")
            cur.execute("INSERT INTO cart(user_id, total_price, state) VALUES ({}, 0, '{}')".format(data['userId'], 'ACTIVE'))
        logger.info("Executing SELECT query on cart to load the logged in user's cart")
        cur.execute("SELECT * FROM cart where user_id = {} and state = '{}'".format(data['userId'], 'ACTIVE'))
        logger.info("Fetching the user's cart")
        cart = cur.fetchone()
        logger.info("Executing INSERT query on cart_items to insert the product into the cart")
        cur.execute("INSERT INTO cart_items(cart_id, product_id, quantity) VALUES ({0}, {1}, {2})".format(cart['cart_id'], data['productId'], 1))
        logger.info("Making a request on Catalogue service to obtain the price of the product")
        headers = {'content-type': 'application/json'}
        url = 'http://catalogue:5001/price'
        data = {"productId": data['productId']}
        data = json.dumps(data)
        response = requests.post(url, data=data, headers=headers)        
        logger.info("Response from Catalogue: {}".format(response.status_code))
        if response.status_code is 200:
           data = json.loads(response.content)
           cur.execute("UPDATE cart SET total_price = total_price + {} where cart_id = {}".format(data['price'], cart['cart_id']))
        else:
           respons.status = 500
           return response
        logger.info("Committing the changes")
        mysql.connection.commit()
        cur.close()
        logger.info("Leaving Cart service successfully")
        response = Response(status=200)
    except:
        logger.debug("Execution failed. Leaving Cart service")
        response = Response(status=500)
    # flash('You have successfully added this product to your cart','success')
    # return redirect(url_for('index'))
    return response

@app.route('/cart', methods=['POST'])
# ToDo: List products and remove duplication of cart items, handle case for result zero
def cart():
    logger.info("Entered Cart service to display cart items")
    data = json.loads(request.data)
    try:
        logger.info("Creating a MySQL cursor")
        cur = mysql.connection.cursor()
        #
        logger.info("Executing SELECT query on cart items to load the cart")
        result = cur.execute("SELECT * FROM cart_items where cart_id in \
                                (SELECT cart_id from cart where user_id={} and state='{}')".format(data['userId'], 'ACTIVE'))
        if result > 0:
            logger.info("Fetching cart items")
            cart = cur.fetchall()
            headers = {'content-type': 'application/json'}
            #url = 'http://catalogue:5001/'
            #logger.info("Making a request on Catalogue service to receive the price of products")        
            #response = requests.post(url, headers=headers)
            #logger.debug("Response from Catalogue: {}".format(response.status_code))
            #if response.status_code is 200:
                #logger.info("Loading product details")
                #products = json.loads(response.content)['productDetails']
                #totalPrice = 0
                #logger.debug("Calculating price of each cart item in cart")
                #for cartItem in cart:
                    #productId = cartItem['product_id']
                    #for product in products:
                        #if productId is product['product_id']:
                            #totalPrice += product['price']
                #data = {'cart': cart, 'totalPrice': totalPrice}
           # url = 'http://catalogue:5001/price'
           # logger.info("Making a request on Catalogue to obtain the price of each product")
           # totalPrice = 0
           # for cartItem in cart:
            #   productId = cartItem['product_id']
            #   data = {"productId": productId}
            #   data = json.dumps(data)
            #   response = requests.post(url, data=data, headers=headers)
            #   logger.info("Response from Catalogue: {}".format(response.status_code))
            #   if response.status_code is 200:
            #      data = json.loads(response.content)
            #      totalPrice += data['price']
            #   else:
            #      logger.info("Execution on Catalogue failed. Leaving Cart service")
            #      response.status_code = 500
            #      return response
            cur.execute("SELECT total_price FROM cart where cart_id = {}".format(cart[0]['cart_id']))
            totalPrice = cur.fetchone()
            totalPrice = totalPrice['total_price']
            logger.info("Leaving Cart service successfully")
            data = {'cart': cart, 'totalPrice': totalPrice}
            return(jsonify(data)), 200

        #     return render_template('cart.html', cart=cart)
        # else:
        #     return "CART EMPTY"
    except:
        logger.info("Execution failed. Leaving cart service")
        response = Response(status=500)
        return response

@app.route('/get-cart-id', methods=['POST'])
def getCartId():
    logger.info("Entered Cart to fetch user's cart IDs")
    data = json.loads(request.data)
    try:
        logger.info("Creating a MySQL cursor")
        cur = mysql.connection.cursor()
        logger.info("Executing SELECT query to fetch cart ID")
        result = cur.execute("SELECT cart_id FROM cart where user_id = {}".format(data['userId']))
        cartIds = cur.fetchall()
        data = {'cartIds': cartIds}
        return jsonify(data), 200
    except:
        return 500

@app.route('/change-state', methods=['POST'])
def changestate():
   logger.info("Entered Cart service to change state")
   data = json.loads(request.data)
   try:
      logger.info("Creating a MySQL cursor")
      cur = mysql.connection.cursor()
      logger.info("Executing UPDATE query to update the state of the cart")
      result = cur.execute("UPDATE cart SET state = '{}' where cart_id = {}".format('INACTIVE', data['cartId']))
      mysql.connection.commit()
      cur.close()
      logger.info("Leaving Cart successfully")
      response = Response(status=200)
   except:
      logger.info("Failed to update cart state. Leaving Cart.")
      response = Response(status=500)
   return response

app.run(port=5003, debug=True, host='0.0.0.0')
