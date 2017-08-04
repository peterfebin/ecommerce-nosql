from flask import Flask, request, Response, jsonify
from flask_mysqldb import MySQL
import json
import requests

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'cart'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/add-to-cart', methods=['POST'])
def addToCart():
    data = json.loads(request.data)
    try:
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM cart where user_id = {}".format(data['userId']))
        if result == 0:
            cur.execute("INSERT INTO cart(user_id) VALUES ({})".format(data['userId']))

        cur.execute("SELECT * FROM cart where user_id = {}".format(data['userId']))
        cart = cur.fetchone()
        cur.execute("INSERT INTO cart_items(cart_id, product_id, quantity) VALUES ({0}, {1}, {2})".format(cart['cart_id'], data['productId'], 1))
        mysql.connection.commit()
        cur.close()
        response = Response(status=200)
    except:
        response = Response(status=500)
    # flash('You have successfully added this product to your cart','success')
    # return redirect(url_for('index'))
    return response

@app.route('/cart', methods=['POST'])
# ToDo: List products and remove duplication of cart items
def cart():
    data = json.loads(request.data)
    try:
        cur = mysql.connection.cursor()
        #
        result = cur.execute("SELECT * FROM cart_items where cart_id in \
                                (SELECT cart_id from cart where user_id={})".format(data['userId']))
        if result > 0:
            cart = cur.fetchall()
            headers = {'content-type': 'application/json'}
            url = 'http://127.0.0.1:5001/'
            response = requests.post(url, headers=headers)
            print('RESPONSE: ', response.status_code)
            if response.status_code is 200:
                products = json.loads(response.content)['productDetails']
                totalPrice = 0
                for cartItem in cart:
                    productId = cartItem['product_id']
                    for product in products:
                        if productId is product['product_id']:
                            totalPrice += product['price']
                data = {'cart': cart, 'totalPrice': totalPrice}
            return(jsonify(data)), 200

        #     return render_template('cart.html', cart=cart)
        # else:
        #     return "CART EMPTY"
    except:
        response = Response(status=500)
    return response

@app.route('/get-cart-id', methods=['POST'])
def getCartId():
    data = json.loads(request.data)
    try:
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT cart_id FROM cart where user_id = {}".format(data['userId']))
        result = cur.fetchone()
        cartId = result['cart_id']
        data = {'cartId': cartId}
        return jsonify(data), 200
    except:
        return 500

app.run(port=5003, debug=True)
