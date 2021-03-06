"""
This module handle command.
Loaddb command to create and insert data into database
"""
import datetime
from hashlib import sha256
import yaml
from rich.console import Console
from rich.progress import (
    track,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    Progress,
)
import click
from .app import app, db
from .models import USER, MESSAGE, TICKET, DEVICE, SUBSCRIPTION

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeRemainingColumn(),
)


def create_tables(console: Console):
    """
    Create tables
    """
    tasks = ["Database BIKEEPER"]

    with console.status("[bold green]Creating Database...") as status:
        while tasks:
            task = tasks.pop(0)
            db.drop_all()
            db.create_all()
            console.log(f"{task} created")


def decode_datetime(datetime_str: str) -> datetime:
    """
    Convert string representation of python to datetime
    """
    times = datetime_str.strip("datetime.datetime()").split(",")
    year = int(times[0])
    month = int(times[1])
    day = int(times[2])
    hour = int(times[3])
    minute = int(times[4])
    second = int(times[5])
    microsecond = int(times[6])

    return datetime.datetime(year, month, day, hour, minute, second, microsecond)


def insert_user(user_to_add):
    """
    Add user to database
    :params: user
    """
    user_to_add = user_to_add["user"]

    username = user_to_add["username"]
    num = user_to_add["num"]
    firstname = user_to_add["firstname"]
    lastname = user_to_add["lastname"]
    email = user_to_add["email"]
    town = user_to_add["town"]
    postal_code = user_to_add["postal_code"]
    street = user_to_add["street"]
    profile_picture = user_to_add["profile_picture"]
    is_admin = user_to_add["is_admin"]
    selected_device = user_to_add["selected_device"]
    is_account_blocked = user_to_add["is_account_blocked"]
    date_creation_user = datetime.datetime.now()
    name_subscription = user_to_add["name_subscription"]

    password = sha256()
    password.update(username.encode())  # taking username as password to test

    db.session.add(USER(username, password.hexdigest(), num, firstname, lastname, email, town,
                        postal_code, street, profile_picture, is_admin, selected_device,
                        is_account_blocked, date_creation_user, name_subscription))


def insert_ticket(ticket_to_add):
    """
    Add ticket to database
    :params: ticket
    """
    ticket_to_add = ticket_to_add["ticket"]
    title_ticket = ticket_to_add["title_ticket"]
    is_closed_ticket = ticket_to_add["is_closed_ticket"]
    user = ticket_to_add["user"]

    db.session.add(TICKET(title_ticket, is_closed_ticket, user))


def insert_message(message_to_add):
    """
    Add message to database
    :params: message
    """
    print(message_to_add)
    message_to_add = message_to_add["message"]

    is_admin_message = message_to_add["is_admin_message"]
    datetime_message = decode_datetime(message_to_add["datetime_message"])

    content_message = message_to_add["content_message"]
    id_ticket = message_to_add["id_ticket"]
    username_user = message_to_add["username_user"]

    db.session.add(MESSAGE(
        is_admin_message,
        datetime_message,
        content_message,
        id_ticket,
        username_user))


def insert_device(device_to_add):
    """
    Add device to database
    :params: device
    """
    device_to_add = device_to_add["device"]
    num_device = device_to_add["num_device"]
    name_device = device_to_add["name_device"]
    row_parameters_device = device_to_add["row_parameters_device"]
    user = device_to_add["user"]
    db.session.add(DEVICE(num_device, name_device, row_parameters_device, user))


def insert_subscription(subscription_to_add):
    """
    Add subscription to database
    :params: subscription
    """
    subscription_to_add = subscription_to_add["subscription"]
    name_subscription = subscription_to_add["name_subscription"]
    price_subscription = subscription_to_add["price_subscription"]
    localisation_subscription = subscription_to_add["localisation_subscription"]
    features_subscription = subscription_to_add["features_subscription"]

    plain_text_features_subscription = ""

    if features_subscription is not None:
    
        for feature in features_subscription:
            plain_text_features_subscription += feature + ";"

    db.session.add(SUBSCRIPTION(name_subscription, price_subscription, localisation_subscription, plain_text_features_subscription))


def import_data(filename: str):
    """
    Load data in yml file into database
    :params: filename, filename of data
    """

    def switch(case):
        return {
            "subscriptions": insert_subscription,
            "users": insert_user,
            "device": insert_device,
            "messages": insert_message,
            "tickets": insert_ticket
        }.get(case)

    with open(filename) as file:
        documents = yaml.full_load(file)

        for item, doc in documents.items():
            print("Importing : " + item)

            for elem in track(doc):
                switch(item)(elem)


@app.cli.command()
def loaddb():
    """
    Create all tables and insert data in database.
    """
    console = Console()
    create_tables(console)
    import_data("./website/data.yml")

    db.session.commit()


@app.cli.command()
def removedb():
    """
    Remove all table from database.
    """
    db.session.remove()
    print("Removing database")
    db.drop_all()


@app.cli.command("adduser")
@click.argument("username")
@click.argument("num")
@click.argument("email")
@click.argument("profile_picture")
def adduser(username, num, email, profile_picture):
    """
    Create all tables and insert data in database.
    """

    password = sha256()
    password.update(username.encode())  # taking username as password to test

    db.session.add(USER(username, password.hexdigest(), num, "John", "Doe", email, "town",
                        "12345", "street", profile_picture, False, False, datetime.datetime.now(), "France"))

    db.session.commit()
