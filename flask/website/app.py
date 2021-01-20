import sqlalchemy
from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


login_manager = LoginManager(app)
login_manager.login_view = "login"

app.config.update(
    SECRET_KEY="GH5H-QLPE4-MPN3-1THB",
    SEND_FILE_MAX_AGE_DEFAULT=0,
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    DEBUG_TB_INTERCEPT_REDIRECTS=False
)

toolbar = DebugToolbarExtension(app)

Mobility(app)


def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))


# MariaDB Config
SERVER_IP = "10.0.0.24"  # ip 92.188.70.221
SERVER_USER = "root"
SERVER_PASSWORD = "bikeeper"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/BIKEEPER'.format(SERVER_USER, SERVER_PASSWORD,
                                                                                   SERVER_IP)

# Module that will build python objects
db = SQLAlchemy(app)
# db.init_app(app)
# Engine connecting to MariaDB
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)# , isolation_level="READ
# UNCOMMITTED"
# db.metadata.create_all(engine)

# Session that is used to perform sql requests to the engine -> here MariaDB
Session = sessionmaker(bind=engine)
session = Session()

from website.views import home
from website.views import settings
from website.views import login
from website.views import register
from website.views import index
from website.views import logout
from website.views import support
from website.views import users
from website.views import admin
from website.api import api
from website.views import stats
from website.views import test

app.register_blueprint(home.mod)
app.register_blueprint(settings.mod)
app.register_blueprint(login.mod)
app.register_blueprint(register.mod)
app.register_blueprint(index.mod)
app.register_blueprint(logout.mod)
app.register_blueprint(support.mod)
app.register_blueprint(users.mod)
app.register_blueprint(api.mod)
app.register_blueprint(admin.mod)
app.register_blueprint(stats.mod)
app.register_blueprint(test.mod)

