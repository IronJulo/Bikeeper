from flask import render_template, request, redirect, url_for, escape
from flask import Blueprint
from hashlib import sha256
from ..models import ORM
from flask_mobility.decorators import mobile_template
from ..app import db
from ..models import USER, DEVICE
from flask.helpers import flash
import datetime
from ..utils import Utils

mod = Blueprint('register', __name__)


@mod.route('/register/', methods=['GET', 'POST'])
@mobile_template('{mobile/Authentification/}register.html')
def register(template):
    subscriptions = ORM.get_subscriptions()
    features = Utils.str_collon_to_list(ORM.get_subscriptions_features()[0])
    return render_template(
        template,
        subscriptions = subscriptions,
        features = features
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
    selected_device = ORM.get_new_num_device()
    is_account_blocked = False
    date_creation_user = datetime.datetime.now()
    name_subscription = str(escape(request.form['sub']))

    informations = {
        "username" : username,
        "email" : email,
        "password" : password,
        "confirmpassword" : confirmpassword,
        "phonenumber" : phonenumber,
        "address" : address,
        "city" : city,
        "postalcode" : postalcode,
    }

    valid, message = ORM.is_valid_register(informations)

    if valid:
        m = sha256()
        m.update(password.encode())
        u = USER(
            username, m.hexdigest(), phonenumber, "", "", email, city, postalcode, address,
                f"https://eu.ui-avatars.com/api/{username}", False, selected_device, is_account_blocked,
                date_creation_user, name_subscription)
        db.session.add(u)

        d = DEVICE(selected_device, Utils.read_prefixes(), None, username)
        db.session.add(d)

        db.session.commit()

        flash(message,"success")
        return redirect(url_for('login.login'))
    else:
        flash(message,"error")
        return redirect(url_for('register.register'))
    
