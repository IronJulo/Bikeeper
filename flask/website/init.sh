#!/bin/bash

echo Create virtual env...
python3.8 -m venv env
echo Done
echo Enter in vitualenv
source env/bin/activate

pip3 install -r requirements.txt