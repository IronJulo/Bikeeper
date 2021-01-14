from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)
from ..models import ORM
from flask_mobility.decorators import mobile_template

mod = Blueprint('support', __name__)


@mod.route('/support/', methods=['GET'])
def support():
    messages = {}
    for ticket in ORM.get_open_ticket():
        messages[ticket.id_ticket] = ORM.get_message_by_ticket_id(ticket.id_ticket)

    return render_template(
        "support.html",
        messages = messages,
    )

@mod.route('/support/add/message', methods=['GET'])
def support_add_message():
    return render_template("support.html")

@mod.route('/support/<int:admin_id>/tickets/all', methods=['GET'])
def get_tickets_admin_by_id(admin_id):
    return ""


@mod.route('/support/<int:user_id>/tickets/all', methods=['GET'])
def get_user_tickets_by_id(user_id):
    res = "<ul>"
    list_ticket = ORM.get_user_tickets(user_id)
    for ticket in list_ticket:
        res += f"<li><p>ID ticket: {ticket.id_ticket}</p>" \
               f"<p>Title ticket: {ticket.title_ticket}" \
               f"<p>Is closed?: {ticket.is_closed_ticket}</p></li>"
    res += "</ul>"
    return res

@mod.route('/support/tickets/open/all', methods=['GET'])
def get_open_tickets():
    res = "<ul>"
    open_tickets = ORM.get_open_ticket()
    print(open_tickets)
    for ticket in open_tickets:
        res += f"<li><p>ID ticket: {ticket.id_ticket}</p>" \
               f"<p>Title ticket: {ticket.title_ticket}" \
               f"<p>Is closed?: {ticket.is_closed_ticket}</p></li>"
    res += "</ul>"
    return res