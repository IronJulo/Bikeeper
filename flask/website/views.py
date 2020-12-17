from .app import app
from .models import orm_get_user, orm_get_user_tickets, orm_get_user_message_title
from flask import render_template, request, redirect
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from flask_mobility.decorators import mobilized


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")


#
@app.route('/login', methods=['GET', 'POST'])
@mobile_template("{mobile/Authentification/}login.html")
def login(template):
    print("Template : ", template)
    return render_template(template)


@app.route('/register/', methods=['GET', 'POST'])
@mobile_template('{mobile/Authentification/}register.html')
def register(template):
    return render_template(template)


@app.route('/delivery', methods=['GET'])
def delivery():
    return ""


@app.route('/home/user/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return ""


@app.route('/stats/device/<int:device_id>/<date>', methods=['GET'])
def get_stat_by_device_id(device_id, date):
    return ""


@app.route('/settings/all', methods=['GET'])
def settings():
    return ""


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
    user = orm_get_user(user_id)
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
    list_ticket = orm_get_user_tickets(user_id)
    for ticket in list_ticket:
        res += f"<li><p>ID ticket: {ticket.id_ticket}</p>" \
               f"<p>Title ticket: {orm_get_user_message_title(ticket.id_ticket)}" \
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
