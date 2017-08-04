from flask import Flask, request, Response, jsonify
from flask_mysqldb import MySQL
import json
import requests
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_DB_HOST']
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_DB_PASSWORD']
app.config['MYSQL_DB'] = 'payment'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/payment', methods=['POST'])
def payment():
    data = json.loads(request.data)
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO payment(order_id) VALUES({})".format(data['orderId']))
        mysql.connection.commit()
        cur.close()
        headers = {'content-type': 'application/json'}
        url = 'http://orders:5004/update-order-status'
        data = {"orderId": data['orderId']}
        data = json.dumps(data)
        response = requests.post(url, data=data, headers=headers)
        if response.status_code is 200:
            response = Response(status=200)
            return response
        else:
            response = Response(status=500)
            return response
    except:
        response = Response(status=500)
        return response

    return "SUCCESS"

app.run(port=5005, debug=True, host='0.0.0.0')
