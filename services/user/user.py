from flask import Flask, request, Response
import json
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_DB_HOST']
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_DB_PASSWORD']
app.config['MYSQL_DB'] = 'user'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/register', methods=['POST'])
def register():
    logger.info("Entered User service to register")
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    email = data['email']
    try:
        logger.info("Creating MySQL cursor")
        # Create cursor
        cur = mysql.connection.cursor()
        logger.info("Executing INSERT query on user table")
        cur.execute("INSERT INTO user(username, password, email, type) VALUES (%s, %s, %s, %s)", (username, password, email, "customer"))
        # Commit to DB
        logger.info("Committing the changes")
        mysql.connection.commit()
        # Close connection
        logger.info("Closing the MySQL cursor")
        cur.close()
        response = Response(status=200)
        logger.info("Leaving User service successfully.")
    except:
        logger.warning("Execution failed. Leaving user service")
        response = Response(status=500)
    return response

#ToDo: Convert JSON dumps to jsonify
@app.route('/login', methods=['POST'])
def login():
    logger.info("Entered User service to login")
    data = json.loads(request.data)
    username = data['username']
    password_candidate = data['password_candidate']

    try:
        logger.info("Creating a MySQL cursor")
        # Create cursor
        cur = mysql.connection.cursor()
        logger.info("Executing SELECT query on user table")
        # Get user by username
        result = cur.execute("SELECT * FROM user WHERE username = '{}'".format(username))
        if result > 0:
            # Get stored hash
            logger.info("Fetching the password from table")
            data = cur.fetchone()
            password = data['password']
            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                # session['logged_in'] = True
                # session['username'] = username
                # session['userId'] = data['user_id']
                # flash('You are now logged in', 'success')

                #response = Response(status=200, response='{"a": "b"}')
                userId = data['user_id']
                response = Response(status=200, response=json.dumps({"userId": userId}))
                logger.info("Leaving User service successfully")
                #return redirect(url_for('index'))
            else:
                logger.warning("Passwords do not match. Leaving User Service")
                response = Response(status=401)
                # error = 'Invalid login'
                # return render_template('login.html', error=error)
            cur.close()
        else:
            logger.warning("Username does not exit. Leaving User service")
            response = Response(status=400)
            # error = 'Username not found'
            # return render_template('login.html', error=error)
    except:
        logger.info("Execution failed. Leaving user service")
        response = Response(status=500)
    return response

#return render_template('login.html')
app.run(port=5002, debug=True, host='0.0.0.0')
