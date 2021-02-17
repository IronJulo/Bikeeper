from flask import (
    Blueprint,
    send_from_directory,
)

from ..app import app

mod = Blueprint('images', __name__)


@mod.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@mod.errorhandler(413)
def too_large(e):
    return "File is too large", 413
