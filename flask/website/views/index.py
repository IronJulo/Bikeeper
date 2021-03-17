from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    escape,
)
from flask_mobility.decorators import mobile_template
from flask_login import current_user, logout_user

mod = Blueprint('index', __name__)

@mod.route('/', methods=['GET', 'POST'])
@mobile_template('{mobile/Authentification/}index.html')
def index(template):
    if current_user.is_authenticated:
        logout_user()
    return render_template(template)
