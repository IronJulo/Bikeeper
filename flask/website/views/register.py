from flask import render_template, request, redirect, url_for, escape
from flask import Blueprint
from hashlib import sha256
from ..models import ORM
from flask_mobility.decorators import mobile_template
from ..app import db
from ..models import USER

mod = Blueprint('register', __name__)


@mod.route('/register/', methods=['GET', 'POST'])
@mobile_template('{mobile/Authentification/}register.html')
def register(template):
    return render_template(
        template,
    )


@mod.route('/register/validate/', methods=['GET', 'POST'])
def register_validate():
    username = str(escape(request.form['username']))
    email = str(escape(request.form['email']))
    password = str(escape(request.form['password']))
    confirmpassword = str(escape(request.form['confirmpassword']))
    phonenumber = str(escape(request.form['tel']))
    address = str(escape(request.form['address']))
    city = str(escape(request.form['city']))
    postalcode = str(escape(request.form['postalcode']))

    if password == confirmpassword and ORM.is_username_available(username):
        m = sha256()
        m.update(password.encode())
        u = USER(username, m.hexdigest(), phonenumber, None, None, email, city, postalcode, address,
                 f"https://eu.ui-avatars.com/api/?name={username}", False)
        db.session.add(u)
        db.session.commit()

        return redirect(url_for('login'))

    return redirect(url_for('register'))
