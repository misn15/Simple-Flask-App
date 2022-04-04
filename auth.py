from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import Customer
from flask_login import login_user, current_user
from . import db
import sys

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    cust = Customer.query.filter_by(email=email).first()

    if not cust or not check_password_hash(cust.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(cust, remember=remember)
    return redirect(url_for('main.update_profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/updateProfile", methods=['POST'])
@login_required
def update_customer_partial():
    cust = Customer.query.get_or_404(current_user.id)
    new_cust_name = request.form.get('new_name')
    new_cust_username = request.form.get('new_username')
    new_cust_email = request.form.get('new_email')
    if new_cust_name:
        cust.name = new_cust_name
    if new_cust_username:
        cust.username = new_cust_username
    if new_cust_email:
        cust.email = new_cust_email
    cust = db.session.merge(cust)
    db.session.commit()
    return render_template('updated_profile.html', name=current_user.name, username=current_user.username, email=current_user.email)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')

    cust_email = Customer.query.filter_by(email=email).first() 
    cust_username = Customer.query.filter_by(username=username).first()

    if cust_username:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_customer = Customer(username=username, email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_customer)
    db.session.commit()

    return redirect(url_for('auth.login'))

