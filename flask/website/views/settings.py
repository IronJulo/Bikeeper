from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

mod = Blueprint('settings', __name__)


@mod.route('/settings/', methods=['GET'])
def settings():
    return render_template(
        "settings.html",
    )


@mod.route('/settings/account/', methods=['GET'])
def settings_account():
    return "Not implemented yet"


@mod.route('/settings/devices/', methods=['GET'])
def settings_devices():
    return "Not implemented yet"


@mod.route('/settings/contacts/', methods=['GET'])
def settings_contact():
    return "Not implemented yet"


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
