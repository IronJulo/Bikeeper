from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    Response
)
from ..app import db
from ..models import ORM, TICKET, USER, MESSAGE
from flask_mobility.decorators import mobile_template
from flask_login import login_required, current_user

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

@mod.route('/support/message/new', methods=['POST'])
def support_message_new():
    if request.method == 'POST':
        contenu_message = request.json['content']
        is_admin = request.json['is_admin']
        date = request.json['date']
        id_ticket = request.json['id_ticket']
        print(contenu_message,is_admin,date,id_ticket)

        msg = MESSAGE(is_admin,date,contenu_message,id_ticket)
        db.session.add(msg)
        db.session.commit()

        return Response(status=200)


@mod.route('/support/ticket/new', methods=['POST'])
def support_new_ticket():
    title = request.form.get('ticket')
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = current_user.username_user
    ticket = TICKET(title,0,user)
    db.session.add(ticket)
    db.session.commit()
    return redirect(url_for('support.support'))


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
    for ticket in open_tickets:
        res += f"<li><p>ID ticket: {ticket.id_ticket}</p>" \
               f"<p>Title ticket: {ticket.title_ticket}" \
               f"<p>Is closed?: {ticket.is_closed_ticket}</p></li>"
    res += "</ul>"
    return res