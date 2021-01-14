from .app import app, db
from .models import ORM
from flask import render_template, request, redirect, url_for, escape
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from flask_mobility.decorators import mobilized
from flask_login import login_required, login_user, logout_user, current_user
from .models import USER



@app.context_processor
def global_user():
    return dict(user=current_user)


# @app.route('/login/', methods=['GET', 'POST'])
# @mobile_template("{mobile/Authentification/}login.html")
# def login(template):
#     print("Template : ", template)
#     return render_template(template)


# @app.route('/register/', methods=['GET', 'POST'])
# @mobile_template('{mobile/Authentification/}register.html')
# def register(template):
#     return render_template(template)


@app.route('/guide/', methods=['GET'])
def guide():
    return "Not implemented yet"


@app.route('/plateform/admin', methods=['GET'])
def admin_plateform():
    return "Not implemented yet"


