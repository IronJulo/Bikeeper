from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)
from flask_mobility.decorators import mobile_template

mod = Blueprint('admin', __name__)


@mod.route('/e/', methods=['GET'])
@mobile_template("{mobile/Admin/}admin_access.html")
def admin_access(template):
    return render_template(template)