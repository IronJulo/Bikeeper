from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)
from flask_mobility.decorators import mobile_template

mod = Blueprint('settings', __name__)


@mod.route('/settings/', methods=['GET'])
def settings():
    return render_template(
        "settings.html",
    )

'''
ACCOUNT
'''
@mod.route('/settings/account/', methods=['GET'])
def settings_account():
    return render_template("account.html")

@mod.route('/settings/account/update/', methods=['GET', 'POST'])
def settings_account_update():
    return redirect(url_for("settings.settings_account"))

'''
DEVICES
'''
@mod.route('/settings/devices/', methods=['GET'])
def settings_devices():
    return render_template("device.html")

@mod.route('/settings/devices/update/', methods=['GET'])
def settings_devices_update():
    return redirect(url_for("settings.settings_devices"))

'''
CONTACT
'''
@mod.route('/settings/contacts/', methods=['GET'])
def settings_contact():
    return render_template("contacts.html")

#UPDATE
@mod.route('/settings/contacts/update/', methods=['GET'])
def settings_contact_update():
    return render_template("update_contact.html")

@mod.route('/settings/contacts/update/check/', methods=['GET','POST'])
def settings_contact_update_check():
    return redirect(url_for("settings.settings_contact"))

#ADD
@mod.route('/settings/contacts/add/', methods=['GET'])
def settings_contact_add():
    return render_template("add_contact.html")

@mod.route('/settings/contacts/add/check/', methods=['GET', 'POST'])
def settings_contact_add_check():
    return redirect(url_for("settings.settings_contact"))

#REMOVE
@mod.route('/settings/contacts/remove/', methods=['GET','POST'])
def settings_contact_remove():
    return redirect(url_for('settings.settings_contact'));

@mod.route('/settings/payments/', methods=['GET'])
def settings_payments():
    return "Not implemented yet"


@mod.route('/settings/subscriptions/', methods=['GET'])
def settings_subscriptions():
    return "Not implemented yet"


@mod.route('/settings/account/<string:user_id>', methods=['GET'])
def get_settings_by_user_id(user_id):
    return ""


@mod.route('/settings/bikeeper/<string:user_id>', methods=['GET'])
def get_bikeeper_settings_by_user_id(user_id):
    return ""


@mod.route('/settings/contacts/<user_id>/all', methods=['GET'])
def get_contacts_by_user_id(user_id):
    return ""


@mod.route('/settings/contact/<string:user_id>/<int:contact_id>/update/<int:updated_data>', methods=['POST'])
def edit_contact_by_user_id(user_id, contact_id, updated_data):
    return ""


@mod.route('/settings/plan/<string:user_id>', methods=['GET'])
def get_user_plan_by_id(user_id):
    return ""


@mod.route('/settings/payment/<string:user_id>/update/<updated_data>', methods=['GET'])
def update_payment_by_id(user_id, updated_data):
    return ""


@mod.route('/settings/payment/<string:user_id>', methods=['GET'])
def setting_payment_page(user_id):
    return ""


@mod.route('/settings/contact/<string:user_id>/add/<data>', methods=['POST'])
def add_contact_by_user_id(user_id, data):
    return ""


@mod.route('/settings/account/<string:user_id>/update/<updated_data>', methods=['POST'])
def update_contact_by_user_id(user_id, updated_data):
    return ""
