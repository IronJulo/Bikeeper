from .app import app
from flask import render_template, request, redirect
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template


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


@app.route('/delivery', methods='GET')
def delivery():
    return ""


@app.route('/home/user/<int:user_id>', methods='GET')
def get_user_by_id(user_id):
    return ""


@app.route('/stats/device/<int:device_id>/<date>', methods='GET')
def get_stat_by_device_id(device_id, date):
    return ""


@app.route('/settings/all', methods='GET')
def settings():
    return ""


@app.route('/settings/account/<int:user_id>', methods='GET')
def get_settings_by_user_id(user_id):
    return ""


@app.route('/settings/bikeeper/<int:user_id>', methods='GET')
def get_bikeeper_settings_by_user_id(user_id):
    return ""


@app.route('/settings/contacts/<user_id>/all', methods='GET')
def get_contacts_by_user_id(user_id):
    return ""


@app.route('/settings/contact/<int:user_id>/<int:contact_id>/update/<int:updated_data>', methods='POST')
def edit_contact_by_user_id(user_id, contact_id, updated_data):
    return ""


@app.route('/home/admin', methods='GET')
def admin():
    return


@app.route('/plateform/admin', methods='GET')
def admin_plateform():
    return ""


@app.route('/users/<int:user_id>', methods='GET')
def user_page(user_id):
    return ""


@app.route('/support/<int:admin_id>/tickets/all', methods='GET')
def get_tickets_admin_by_id(admin_id):
    return ""


@app.route('/support/<int:user_id>/tickets/all', methods='GET')
def get_user_tickets_by_id(user_id):
    return ""


@app.route('/settings/plan/<user_id>', methods='GET')
def get_user_plan_by_id(user_id):
    return ""


@app.route('/settings/payment/<int:user_id>/update/<updated_data>', methods='GET')
def update_payment_by_id(user_id, updated_data):
    return ""


@app.route('/settings/payment/<user_id>', methods='GET')
def setting_payment_page(user_id):
    return ""


@app.route('/settings/contact/<int:user_id>/add/<data>', methods='POST')
def add_contact_by_user_id(user_id, data):
    return ""


@app.route('/settings/account/<int:user_id>/update/<updated_data>', methods='POST')
def add_contact_by_user_id(user_id, updated_data):
    return ""
