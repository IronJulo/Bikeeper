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
@mobile_template('{mobile/User/}support.html')
def support(template):
    messages = {}

    if not current_user.is_admin_user:
        open_tickets_user = ORM.get_open_ticket_user(current_user.username_user)

        if len(open_tickets_user) != 0:
            for ticket in open_tickets_user:
                messages[ticket.id_ticket] = ORM.get_message_by_ticket_id(ticket.id_ticket)
    else:
        open_tickets = ORM.get_open_ticket()
        for ticket in open_tickets:
            messages[ticket.id_ticket] = ORM.get_message_by_ticket_id(ticket.id_ticket)
    
    last_messages = {}
    for i_mes in messages.keys():
        last_messages[i_mes] = ORM.get_last_message_by_ticket_id(i_mes)
    
    return render_template(
        template,
        messages = messages,
        picture = ORM.get_picture_message_from_username(current_user.username_user),
        last_messages= last_messages,
        devices = ORM.get_devices_by_username(current_user.username_user)
    )

@mod.route('/support/<int:id_ticket>/', methods=['GET'])
def support_message(id_ticket):
    return render_template(
        'mobile/User/support-bis.html',
        id_ticket = id_ticket,
        messages = ORM.get_message_by_ticket_id(id_ticket),
        picture = ORM.get_picture_message_from_username(current_user.username_user),
        )

@mod.route('/support/message/new', methods=['POST'])
def support_message_new():
    if request.method == 'POST':
        contenu_message = request.json['content']
        is_admin = request.json['is_admin']
        date = request.json['date']
        id_ticket = request.json['id_ticket']
        username = request.json['username']

        msg = MESSAGE(is_admin, date, contenu_message, id_ticket, username)
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