from flask import Flask, request, Response
import json
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'user'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    email = data['email']
    print(username, password, email)
    try:
        # Create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(username, password, email, type) VALUES (%s, %s, %s, %s)", (username, password, email, "customer"))
        # Commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        response = Response(status=200)
    except:
        response = Response(status=500)
    return response

#ToDo: Convert JSON dumps to jsonify
@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    username = data['username']
    password_candidate = data['password_candidate']

    # Create cursor
    cur = mysql.connection.cursor()
    # Get user by username
    try:
        result = cur.execute("SELECT * FROM user WHERE username = '{}'".format(username))
        if result > 0:
            # Get stored hash
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
                #return redirect(url_for('index'))
            else:
                response = Response(status=401)
                # error = 'Invalid login'
                # return render_template('login.html', error=error)
            cur.close()
        else:
            response = Response(status=400)
            # error = 'Username not found'
            # return render_template('login.html', error=error)
    except:
        response = Response(status=500)
    return response

#return render_template('login.html')
app.run(port=5002, debug=True)
