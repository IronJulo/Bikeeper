import requests
import random
import json

for i in range(10):
    url = "http://127.0.0.1:5000/api/sms/add/"
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {"header": {"key": "[bk]", "schema": "+", "sender": "0769342048"},
                "data": {"type": "C"}}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    for i in range(25):
        lon = 4.156874215876547
        lat = 5.156874215876547
        lon += random.random()
        lat += random.random()
        payload = {"header": {"key": "[bk]", "schema": "*", "sender": "0769342048"},
                "data": {"longitude": lon, "latitude": lat, "charge": "f", "level": [50, 42]}}


        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        print(response.text)

    payload = {"header": {"key": "[bk]", "schema": "+", "sender": "0769342048"},
                "data": {"type": "D"}}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))