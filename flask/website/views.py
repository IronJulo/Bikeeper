from .app import app, db
from .models import ORM
from flask import render_template, request, redirect, url_for, escape
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from flask_mobility.decorators import mobilized
from flask_login import login_required, login_user, logout_user, current_user
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from .models import USER
from hashlib import sha256


@app.context_processor
def global_user():
    return dict(user=current_user)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


# @app.route('/login/', methods=['GET', 'POST'])
# @mobile_template("{mobile/Authentification/}login.html")
# def login(template):
#     print("Template : ", template)
#     return render_template(template)


# @app.route('/register/', methods=['GET', 'POST'])
# @mobile_template('{mobile/Authentification/}register.html')
# def register(template):
#     return render_template(template)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    next = HiddenField()

    def get_data(self):
        return self.username.data

    def get_authenticated_user(self):
        user = ORM.load_user(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password_user else None


@app.route('/login/', methods=['GET', 'POST'])
@mobile_template("{mobile/Authentification/}login.html")
def login(template):
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template(
        template,
        form=f,
    )


@app.route('/register/', methods=['GET', 'POST'])
@mobile_template('{mobile/Authentification/}register.html')
def register(template):
    return render_template(
        template,
    )


@app.route('/register/validate/', methods=['GET', 'POST'])
def register_validate():
    username = str(escape(request.form['username']))
    email = str(escape(request.form['email']))
    password = str(escape(request.form['password']))
    confirmpassword = str(escape(request.form['confirmpassword']))
    phonenumber = str(escape(request.form['tel']))
    address = str(escape(request.form['address']))
    city = str(escape(request.form['city']))
    postalcode = str(escape(request.form['postalcode']))

    print(ORM.is_username_available(username))
    if password == confirmpassword and ORM.is_username_available(username):
        m = sha256()
        m.update(password.encode())
        u = USER(username, m.hexdigest(), phonenumber, None, None, email, city, postalcode, address,
                 f"https://eu.ui-avatars.com/api/?name={username}", False)
        db.session.add(u)
        db.session.commit()

        return redirect(url_for('login'))

    return redirect(url_for('register'))


@app.route('/home/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/statistics/', methods=['GET'])
def statistics():
    return "Not implemented yet"


@app.route('/delivery', methods=['GET'])
def delivery():
    return ""


@app.route('/home/user/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return ""


@app.route('/stats/device/<int:device_id>/<date>', methods=['GET'])
def get_stat_by_device_id(device_id, date):
    return ""


@app.route('/support/', methods=['GET'])
def support():
    return "Not implemented yet"


@app.route('/settings/', methods=['GET'])
def settings():
    return "Not implemented yet"


@app.route('/devices/', methods=['GET'])
def devices():
    return "Not implemented yet"


@app.route('/guide/', methods=['GET'])
def guide():
    return "Not implemented yet"


@app.route('/settings/account/<string:user_id>', methods=['GET'])
def get_settings_by_user_id(user_id):
    return ""


@app.route('/settings/bikeeper/<string:user_id>', methods=['GET'])
def get_bikeeper_settings_by_user_id(user_id):
    return ""


@app.route('/settings/contacts/<user_id>/all', methods=['GET'])
def get_contacts_by_user_id(user_id):
    return ""


@app.route('/settings/contact/<string:user_id>/<int:contact_id>/update/<int:updated_data>', methods=['POST'])
def edit_contact_by_user_id(user_id, contact_id, updated_data):
    return ""


@app.route('/home/admin', methods=['GET'])
def admin():
    return


@app.route('/plateform/admin', methods=['GET'])
def admin_plateform():
    return ""


@app.route('/users/<string:user_id>', methods=['GET'])
def user_page(user_id):
    user = ORM.get_user(user_id)
    return f"<p>Username: {user.username_user}</p>" \
           f"<p>Number: {user.num_user}</p>" \
           f"<p>Firstname: {user.firstname_user}</p>" \
           f"<p>Lastname: {user.lastname_user}</p>" \
           f"<p>Email: {user.email_user}</p>" \
           f"<p>Town: {user.town_user}</p>" \
           f"<p>Postal code: {user.postal_code_user}</p>" \
           f"<p>Street: {user.street_user}</p>"


@app.route('/support/<int:admin_id>/tickets/all', methods=['GET'])
def get_tickets_admin_by_id(admin_id):
    return ""


@app.route('/support/<string:user_id>/tickets/all', methods=['GET'])
def get_user_tickets_by_id(user_id):
    res = "<ul>"
    list_ticket = ORM.get_user_tickets(user_id)
    for ticket in list_ticket:
        res += f"<li><p>ID ticket: {ticket.id_ticket}</p>" \
               f"<p>Title ticket: {ticket.title_ticket}" \
               f"<p>Is closed?: {ticket.is_closed_ticket}</p></li>"
    res += "</ul>"
    return res


@app.route('/settings/plan/<string:user_id>', methods=['GET'])
def get_user_plan_by_id(user_id):
    return ""


@app.route('/settings/payment/<string:user_id>/update/<updated_data>', methods=['GET'])
def update_payment_by_id(user_id, updated_data):
    return ""


@app.route('/settings/payment/<string:user_id>', methods=['GET'])
def setting_payment_page(user_id):
    return ""


@app.route('/settings/contact/<string:user_id>/add/<data>', methods=['POST'])
def add_contact_by_user_id(user_id, data):
    return ""


@app.route('/settings/account/<string:user_id>/update/<updated_data>', methods=['POST'])
def update_contact_by_user_id(user_id, updated_data):
    return ""


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
