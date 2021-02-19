import unittest
import requests


def post(url, data):
    headers = {
        'Content-type': 'application/json',
    }
    # data = '{"text":"Hello, World!"}'
    response = requests.post(url, headers=headers, data=data)
    return response.json()

def get(url):
    response=requests.get(url)
    return response.json()

class TestAPI(unittest.TestCase):

    def test_send_sms(self):
        data = '{"header":{"key": "[bk]", "schema": "@", "sender": "06...."}, "data":{"text":"Hello, World!"}'
        res=post('http://127.0.0.1:5000/api/sms/add/',data)
        print('-'*100)
        print(res)
        print('-'*100)
        
        self.assertEqual('error', res['type_message'])
        # data='{"key": "[bk]", "schema": "@", "sender": "06...."}'
        # self.assertEqual('ok', post('http://127.0.0.1:5000/api/sms/add/',data)['type_message'])

    def test_add_device(self):
        data1 = '{"num_device": "7474412315","name_device": "CestPourLesTests","row_parameters_device": "","user": "user1"}'
        self.assertEqual('ok', post('http://127.0.0.1:5000/api/bikeeper/add/',data1)['type_message'])
        data2 = '{"name_device": "CestPourLesTests2","row_parameters_device": "","user": "user1"}'
        self.assertEqual('error', post('http://127.0.0.1:5000/api/bikeeper/add/',data2)['type_message'])

        self.assertEqual('ok', post('http://127.0.0.1:5000/api/bikeeper/add_raw/',data1)['type_message'])
        self.assertEqual('error', post('http://127.0.0.1:5000/api/bikeeper/add_raw/',data2)['type_message'])

    def test_update_device(self):
        data1 = '{"num_device": "7474412315","name_device": "CestPourLeTest","row_parameters_device": "","user": "user1"}'
        self.assertEqual('error', post('http://127.0.0.1:5000/api/bikeeper/settings/7474412315/update/',data1)['type_message'])
        data2='{"row_parameters_device": ""}'
        self.assertEqual('ok', post('http://127.0.0.1:5000/api/bikeeper/settings/7474412315/update/',data2)['type_message'])

    def test_get_current_user(self):
        self.assertEqual("0789101112", get('http://127.0.0.1:5000/api/bikeeper/currentphone/7474412315/')['current_phone'])
        self.assertEqual("0789101162", get('http://127.0.0.1:5000/api/bikeeper/currentphone/0664277796/')['current_phone'])

        
if __name__ == '__main__':
    unittest.main()
