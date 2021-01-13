from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

mod = Blueprint("stats", __name__)

@mod.route('/statistics/', methods=['GET'])
def statistics():
    return render_template("stats.html")