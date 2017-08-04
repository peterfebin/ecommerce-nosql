from flask import Flask, Response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'catalogue'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', methods=['POST'])
def catalogue():
    print("HIT")
    cur = mysql.connection.cursor()
    try:
        result = cur.execute("SELECT * from product")
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
        return jsonify({'productDetails': products}), 200
    except:
        response = Response(status=500)

    return response


app.run(port=5001, debug=True)
