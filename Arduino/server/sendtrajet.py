import requests
import random
import json

sender = "0769342048"

for i in range(10):
    url = "http://127.0.0.1:5000/api/sms/add/"
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {"header": {"key": "[bk]", "schema": "+", "sender": sender},
                "data": {"type": "C"}}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    lon = 1.908894000000000
    lat = 47.90176300000000
    speed = 50
    angle = 0
    for i in range(25):
        sign = 1 if random.random() < 0.5 else -1
        lon += random.random() * sign * 0.01
        sign = 1 if random.random() < 0.5 else -1
        lat += random.random() * sign * 0.01
        speed += random.randint(-9, 9)
        angle += random.randint(-1, 1)
        payload = {"header": {"key": "[bk]", "schema": "@", "sender": sender},
                "data": {"longitude": lon, "latitude": lat, "charge": "f", "level": [50, 42], "speed": speed, "angle": angle}}


        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        print(response.text)

    payload = {"header": {"key": "[bk]", "schema": "+", "sender": sender},
                "data": {"type": "D"}}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))