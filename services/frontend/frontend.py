from flask import Flask, render_template, session
# From register
from flask import request, render_template, flash, redirect, url_for, Response
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from forms.register import RegisterForm
import json
import requests
from functools import wraps

app = Flask(__name__)

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login!', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def index():
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:5001/'
    response = requests.post(url, headers=headers)
    if response.status_code is 200:
        products = json.loads(response.content)['productDetails']
        return render_template('index.html', products=products)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        data = {"email": form.email.data, "username": form.username.data, "password": sha256_crypt.encrypt(str(form.password.data))}
        data = json.dumps(data)
        headers = {'content-type': 'application/json'}
        url = 'http://127.0.0.1:5002/register'
        response = requests.post(url, data=data, headers=headers)
        if response.status_code is 200:
            flash('You are now registered and can login', 'success')
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        data = {"username": username, "password_candidate": password_candidate}
        data = json.dumps(data)
        headers = {'content-type': 'application/json'}
        url = 'http://127.0.0.1:5002/login'
        response = requests.post(url, data=data, headers=headers)
        if response.status_code is 200:
            content = json.loads(response.content)
            session['userId'] = content['userId']
            session['logged_in'] = True
            flash('You are now logged in', 'success')
            return redirect(url_for('index'))
        else:
            error = 'Invalid login'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("You have been logged out", 'success')
    return redirect(url_for('login'))

@app.route('/add-to-cart/<int:id>')
@is_logged_in
def addToCart(id):
    productId = id
    data = {"productId": productId, "userId": session['userId']}
    data = json.dumps(data)
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:5003/add-to-cart'
    response = requests.post(url, data=data, headers=headers)
    print(response.status_code)
    if response.status_code is 200:
        flash('You have successfully added this product to your cart','success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/cart')
@is_logged_in
def cart():
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:5003/cart'
    data = {"userId": session['userId']}
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    if response.status_code is 200:
        cart = json.loads(response.content)['cart']
        totalPrice = json.loads(response.content)['totalPrice']
        return render_template('cart.html', cart=cart, totalPrice= totalPrice)
    return 'CART EMPTY'

#ToDo: Add error message
@app.route('/place-order/<int:cartId>/<float:totalPrice>')
@is_logged_in
def placeOrder(cartId, totalPrice):
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:5004/place-order'
    data = {"cartId": cartId, "totalPrice": totalPrice}
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    if response.status_code is 200:
        orderId = json.loads(response.content)['orderId']
        return render_template('place-order.html', orderId=orderId)
    return 'No orders placed'

@app.route('/orders')
@is_logged_in
def orders():
    data = {"userId": session['userId']}
    data = json.dumps(data)
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:5003/get-cart-id'
    response = requests.post(url, data=data, headers=headers)
    if response.status_code is 200:
        data = response.content
        url = 'http://127.0.0.1:5004/orders'
        response = requests.post(url, data=data, headers=headers)
        if response.status_code is 200:
            data = json.loads(response.content)
            return render_template('orders.html', orders=data)
    return render_template('index.html')

@app.route('/payment/<int:id>')
@is_logged_in
def payment(id):
    orderId = id
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:5005/payment'
    data = {"orderId": orderId}
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    if response.status_code is 200:
        return render_template('payment.html')
    return 'No Payments'


app.secret_key='secret'
app.run(port=5000, debug=True)
