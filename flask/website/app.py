import sqlalchemy
from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "login"

app.config["SECRET_KEY"]="GH5H-QLPE4-MPN3-1THB"

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

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
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
db.metadata.create_all(engine)

# Session that is used to perform sql requests to the engine -> here MariaDB
Session = sessionmaker(bind=engine)
session = Session()
