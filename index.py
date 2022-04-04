from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template
from .models import Customer
from flask_login import login_required, current_user
from flask import Blueprint
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/updateProfile')
@login_required
def update_profile():
    return render_template('updated_profile.html', name=current_user.name, username=current_user.username, email=current_user.email)


