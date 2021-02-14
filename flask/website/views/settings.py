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
@mobile_template("{mobile/Settings/}settings.html")
def settings(template):
    return render_template(
        template
    )


"""
ACCOUNT
"""


@mod.route('/settings/account/', methods=['GET'])
@mobile_template("{mobile/Settings/}account.html")
def settings_account(template):
    return render_template(template)


@mod.route('/settings/account/update/', methods=['GET', 'POST'])
def settings_account_update(template):
    return "" #TODO Mathieu


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
@mobile_template("{mobile/Settings/}contacts.html")
def settings_contact(template):
    return render_template(template)


@mod.route('/settings/contacts/update/', methods=['GET'])
def settings_contact_update():
    return render_template("update_contact.html")


@mod.route('/settings/contacts/update/check/', methods=['GET', 'POST'])
def settings_contact_update_check():
    return redirect(url_for("settings.settings_contact"))


@mod.route('/settings/contacts/add/', methods=['GET'])
def settings_contact_add():
    return render_template("add_contact.html")


@mod.route('/settings/contacts/add/check/', methods=['GET', 'POST'])
def settings_contact_add_check():
    return redirect(url_for("settings.settings_contact"))


@mod.route('/settings/contacts/remove/', methods=['GET', 'POST'])
def settings_contact_remove():
    return redirect(url_for('settings.settings_contact'))



'''
CREDIT CARD MOBILE
'''


@mod.route('/settings/card/', methods=['GET'])
def settings_card():
    return render_template("mobile/Settings/credit-card.html")


'''
PAYMENT
'''


@mod.route('/settings/payment/', methods=['GET'])
def settings_payment():
    return render_template('payment.html')


@mod.route('/settings/payment/edit/', methods=['GET', 'POST'])
def settings_payment_edit():
    return render_template('edit_payment.html')


@mod.route('/settings/payment/edit/check/', methods=['GET', 'POST'])
def settings_payment_edit_check():
    return redirect(url_for('settings.settings_payment'))


@mod.route('/settings/subscriptions/', methods=['GET'])
def settings_subscriptions():
    return render_template("subscription.html")


@mod.route('/settings/subscriptions/cancel/', methods=['GET'])
def settings_subscriptions_cancel():
    return redirect(url_for('logout.logout'))


@mod.route('/settings/subscriptions/change/', methods=['GET'])
def settings_subscriptions_change():
    return redirect(url_for('settings.settings_subscriptions'))
