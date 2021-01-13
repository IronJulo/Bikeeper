from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    escape
)
from flask_mobility.decorators import mobile_template

mod = Blueprint('index', __name__)


@mod.route('/', methods=['GET', 'POST'])
@mobile_template('{mobile/Authentification/}index.html')
def index(template):
    return render_template("template")



