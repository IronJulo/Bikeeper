import sqlalchemy
from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


Mobility(app)


def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))


# MariaDB URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:bikeeper@92.188.70.221/BIKEEPER'

# Module that will build python objects
db = SQLAlchemy(app)

# Engine connecting to MariaDB
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
db.metadata.create_all(engine)

# Session that is used to perform sql requests to the engine -> here MariaDB
Session = sessionmaker(bind=engine)
session = Session()
