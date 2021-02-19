from flask import (
	Blueprint,
	render_template,
	abort

)

mod = Blueprint('errors', __name__)


@mod.route("/<path:invalid_path>")
def missing_resource(invalid_path):
	abort(404, description="Resource not found")


@mod.app_errorhandler(404)
def handle_404(err):
	return render_template('404.html'), 404


@mod.app_errorhandler(403)
def handle_403(err):
	return render_template('403.html'), 403

