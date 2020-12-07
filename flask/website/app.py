from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility

app = Flask(__name__)


Mobility(app)


def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))


app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + mkpath('../myapp.db'))
db = SQLAlchemy(app)
