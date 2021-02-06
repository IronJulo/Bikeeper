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


def ok():
    return jsonify(
        type_message="ok"
    )


def errror(err):
    return jsonify(
        type_message="error",
        error=err
    )


@mod.route('/api/sms/add/', methods=['POST'])
def send_sms_to_bd():
    payload = request.json
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
        return errror("Schema type not supported")
    ORM.new_log(dic, data['schema'], datetime.now(), exception_log, header['sender'])
    return ok()


@mod.route('/api/bikeeper/add/', methods=['POST'])
def add_bikeeper_to_bd():
    data = request.json
    try:
        num = data['num_device']
        name = data['name_device']
        row_parameters = data['row_parameters_device']
        username = data['username']
    except KeyError as keyerror:
        return errror(f"{keyerror}")
    ORM.new_device(num, name, row_parameters, username)
    return ok()


@mod.route('/api/bikeeper/remove/<int:device_id>/', methods=['DELETE'])
def remove_bikeeper(device_id):
    if ORM.remove_device(device_id):
        return ok()
    else:
        return errror("No rows deleted")


@mod.route('/api/bikeeper/settings/<int:device_id>/update/', methods=['POST'])
def update_bikeeper_settings_to_bd(device_id):
    data = request.json
    ORM.get_device(device_id).set_row_parameters(f"{data}")
    return ok()


@mod.route('/api/bikeeper/currentphone/<string:device_id>/', methods=['GET'])
def get_current_user_phone_from_db(device_id):
    current_phone = ORM.get_associated_phone(device_id)
    return jsonify(
        type_message="response_current_phone",
        current_phone=current_phone
    )
