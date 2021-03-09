from flask import (
	Blueprint,
	render_template,
	request,
	redirect,
	url_for,
	escape
)
from flask_login import login_required
from flask_mobility.decorators import mobile_template
from ..models import ORM

mod = Blueprint('documentation', __name__)


@mod.route('/faq/', methods=['GET'])
@mobile_template('{mobile/User/}faq.html')
@login_required
def faq(template):
	data = ORM.get_faq_json()
	topic = set()
	for reponse in data.values():
		topic.add(reponse["topic"])
	return render_template(
		template,
		data=data,
		topic=list(topic)
	)
