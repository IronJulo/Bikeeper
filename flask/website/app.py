import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mobility import Mobility
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask import render_template
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from flask_mail import Mail, Message
import os

app = Flask(__name__)
CORS(app)

login_manager = LoginManager(app)
login_manager.login_view = "login.login"

app.config.update(
	SECRET_KEY="GH5H-QLPE4-MPN3-1THB",
	SEND_FILE_MAX_AGE_DEFAULT=0,
	SQLALCHEMY_TRACK_MODIFICATIONS=True,
	DEBUG_TB_INTERCEPT_REDIRECTS=False,
	MAX_CONTENT_LENGTH=2048 * 2048,
	UPLOAD_EXTENSIONS=['.jpg', '.png', '.gif', '.jpeg'],
	UPLOAD_PATH='./website/static/user_profile_picture/',
	UPLOAD_PATH_CONTACT='./website/static/contact_profile_picture/',
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USERNAME='bikeeper.team@gmail.com',
	MAIL_PASSWORD='bikeeper34',
	MAIL_USE_TLS=False,
	MAIL_USE_SSL=True
)

# toolbar = DebugToolbarExtension(app)

Mobility(app)

mail = Mail(app)


def mkpath(p):
	return os.path.normpath(
		os.path.join(
			os.path.dirname(__file__),
			p))


# MariaDB Config

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/BIKEEPER'.format(os.environ.get('SERVER_USER'),
                                                                                   os.environ.get('SERVER_PASSWORD'),
                                                                                   os.environ.get('SERVER_IP'))

# Module that will build python objects
db = SQLAlchemy(app)
# db.init_app(app)
# Engine connecting to MariaDB
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)  # , isolation_level="READ
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
from website.views import admin
from website.views import errors
from website.api import api
from website.views import stats
from website.views import test
from website.views import images
from website.views import sidebar
from website.views import documentation

app.register_blueprint(home.mod)
app.register_blueprint(settings.mod)
app.register_blueprint(login.mod)
app.register_blueprint(register.mod)
app.register_blueprint(index.mod)
app.register_blueprint(logout.mod)
app.register_blueprint(support.mod)
app.register_blueprint(errors.mod)
app.register_blueprint(api.mod)
app.register_blueprint(admin.mod)
app.register_blueprint(stats.mod)
app.register_blueprint(test.mod)
app.register_blueprint(images.mod)
app.register_blueprint(sidebar.mod)
app.register_blueprint(documentation.mod)
