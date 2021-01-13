from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app,
          title='Bikeeper API',
          version='v0.1',
          doc='/',
          prefix='/api')

a_language = api.model(
    'Language',
    {'language': fields.String('The language.')}
)

languages = []
python = {'language': 'Python'}
languages.append(python)


@api.route('/api/sms/add/<string:data>')
@api.doc(params={'data': {'description': 'New data to save in database', 'in': 'query', 'type': 'string'}})
class SMS(Resource):
    def get(self, data):
        data = str(request.args.get('data'))
        return languages


@api.route('/api/bikeeper/add/<string:data>/')
@api.doc(params={'data': {'description': 'Add bikeeper device.', 'in': 'query', 'type': 'string'}})
class SMS(Resource):
    def post(self, data):
        data = str(request.args.get('data'))
        return languages


@api.route('/api/bikeeper/remove/<int:device_id>/')
@api.doc(params={'device_id': {'description': 'New data to save in database', 'in': 'query', 'type': 'int'}})
class SMS(Resource):
    def get(self, device_id):
        device_id = int(request.args.get('device_id'))
        return languages


@api.route('/api/bikeeper/settings/<int:device_id>/add/<string:data>/')
@api.doc(params={'device_id': {'description': 'device id', 'in': 'query', 'type': 'int'}})
@api.doc(params={'data': {'description': 'Data to add in bikeeper', 'in': 'query', 'type': 'string'}})
class SMS(Resource):
    def post(self, device_id):
        data = int(request.args.get('device_id'))
        return languages


@api.route('/api/bikeeper/settings/<int:device_id>/update/<string:updated_data>/')
@api.doc(params={'device_id': {'description': 'device id', 'in': 'query', 'type': 'int'}})
@api.doc(params={'updated_data': {'description': 'Updated data to add', 'in': 'query', 'type': 'string'}})
class SMS(Resource):
    def post(self, device_id):
        data = int(request.args.get('device_id'))
        return languages


@api.route('/api/bikeeper/currentphone/<string:device_id>/')
@api.doc(params={'device_id': {'description': 'Device id', 'in': 'query', 'type': 'int'}})
class SMS(Resource):
    def get(self, device_id):
        current_phone = int(request.args.get('device_id'))
        return jsonify(
            type_message="response_current_phone",
            current_phone=current_phone
        )


if __name__ == '__main__':
    app.run(debug=True)
