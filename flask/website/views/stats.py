from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from flask_mobility.decorators import mobile_template

mod = Blueprint("stats", __name__)

@mod.route('/statistics/', methods=['GET'])
@mobile_template('{mobile/User/}stats.html')
def statistics(template):
    return render_template(template)