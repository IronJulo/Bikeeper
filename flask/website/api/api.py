from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    jsonify,
    request
)
from ..models import ORM
from datetime import datetime

mod = Blueprint('api', __name__)


@mod.route('/api/sms/add/<data>/', methods=['POST'])
def send_sms_to_bd(payload):
    header = payload['header']  # {"key": "[bk]", "schema": "@", "sender": "06...."}
    data = payload['data']
    exception_log = ""
    if header['schema'] == '@':  # Position
        dic = jsonify(
            type=data['type'],
            longitude=data['longitude'],
            latitude=data['latitude'],
            charge=data['charge'],
            level=data['level']
        )
    elif header['schema'] == 'W':  # Alert
        dic = jsonify(
            longitude=data['longitude'],
            latitude=data['latitude'],
            charge=data['charge'],
            level=data['level'],
            speed=data['speed'],
            angle=data['angle']
        )
    elif header['schema'] == '*':  # Normal
        dic = jsonify(
            longitude=data['longitude'],
            latitude=data['latitude'],
            charge=data['charge'],
            level=data['level']
        )
    else:
        return jsonify(
            type_message="error",
            error="Schema type not supported"
        )
    ORM.new_log(dic, data['schema'], datetime.now(), exception_log, header['sender'])
    return jsonify(
        type_message="ok"
    )


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
