from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    jsonify
)
from ..models import ORM

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


@mod.route('/api/bikeeper/currentphone/<string:device_id>/', methods=['GET'])
def get_current_user_phone_from_db(device_id):
    current_phone = ORM.get_associated_phone(device_id)
    return jsonify(
        type_message="response_current_phone",
        current_phone=current_phone
    )
