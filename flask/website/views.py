from .app import app
from flask import render_template, request, redirect
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template

# from tuto.models import *


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return ""


@app.route('/register', methods=['GET', 'POST'])
@mobile_template('{mobile/}register.html')
def register(template):
    return render_template(template)

