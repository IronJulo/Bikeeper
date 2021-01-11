from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

mod = Blueprint('api', __name__)


@mod.route('/api/sms/add/<data>/', methods=['POST'])
def send_sms_to_bd(data):
    return ""


@mod.route('/api/bikeeper/add/<data>/', methods=['POST'])
def add_bikeeper_to_bd(data):
    return ""


@mod.route('/api/bikeeper/remove/<int:device_id>/', methods=['GET'])
def remove_bikeeper(device_id):
    return ""


@mod.route('/api/bikeeper/settings/<int:device_id>/add/<data>/', methods=['POST'])
def add_bikeeper_settings_to_bd(device_id, data):
    return ""


@mod.route('/api/bikeeper/settings/<int:device_id>/update/<updatedData>/', methods=['POST'])
def update_bikeeper_settings_to_bd(device_id, updated_data):
    return ""
