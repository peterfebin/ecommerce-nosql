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
app.config['MYSQL_DB'] = 'payment'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/payment', methods=['POST'])
def payment():
    logger.info("Entered Payment service to make payment")
    data = json.loads(request.data)
    try:
        logger.info("Creating MySQL cursor")
        cur = mysql.connection.cursor()
        logger.info("Executing INSERT query to insert payment details")
        cur.execute("INSERT INTO payment(order_id) VALUES({})".format(data['orderId']))
        mysql.connection.commit()
        cur.close()
        logger.info("Making a request to Orders to update order status")
        headers = {'content-type': 'application/json'}
        url = 'http://orders:5004/update-order-status'
        data = {"orderId": data['orderId']}
        data = json.dumps(data)
        response = requests.post(url, data=data, headers=headers)
        logger.debug("Response from orders: {}".format(response.status_code))
        if response.status_code is 200:
            logger.info("Leaving Payment successfully")
            response = Response(status=200)
            return response
        else:
            logger.info("Failed to update order status. Leaving Payment")
            response = Response(status=500)
            return response
    except:
        logger.info("Execution on Payment failed. Leaving Payment")
        response = Response(status=500)
        return response

    return "SUCCESS"

app.run(port=5005, debug=True, host='0.0.0.0')
