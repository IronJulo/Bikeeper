import click
from .app import app, db
from rich.console import Console
from rich.progress import track
import datetime
from .models import USER, MESSAGE, TICKET, DEVICE
from hashlib import sha256


@app.cli.command()
def loaddb():
    console = Console()
    tasks = ["Database BIKEEPER"]

    with console.status("[bold green]Creating Database...") as status:
        while tasks:
            task = tasks.pop(0)
            db.drop_all()
            db.create_all()
            console.log(f"{task} created")

    to_import = []

    m = sha256()
    m.update("admin".encode())
    to_import.append(USER(
        username="admin",
        password=m.hexdigest(),
        num="0781546427",
        firstname="John",
        lastname="Doe",
        email="johndoe@gmail.com",
        town="Bourges",
        postal_code="18110",
        street="167 rue des coquelicots",
        profile_picture="https://eu.ui-avatars.com/api/?name=admin",
        is_admin=True))

    m = sha256()
    m.update("admin2".encode())
    to_import.append(USER(
        username="admin2",
        password=m.hexdigest(),
        num="0654321012",
        firstname="Michel",
        lastname="Dupon",
        email="micheldupon@gmail.com",
        town="Lille",
        postal_code="59350",
        street="48 rue des coquelicots",
        profile_picture="https://eu.ui-avatars.com/api/?name=admin2",
        is_admin=True))

    m = sha256()
    m.update("user1".encode())
    user1 = USER(
        username="user1",
        password=m.hexdigest(),
        num="0789101112",
        firstname="Luffy",
        lastname="Monkey D",
        email="mugiwara@gmail.com",
        town="Mont Corvo",
        postal_code="45000",
        street="5 rue du roi des pirates",
        profile_picture="https://yt3.ggpht.com/ytc/AAUvwnhaEBIWRCum_FhM08TUczLBY0I5W5wyWH_sSi6pxg=s900-c-k-c0x00ffffff-no-rj",
        is_admin=False)
    to_import.append(user1)

    m = sha256()
    m.update("user2".encode())
    user2 = USER(
        username="user2",
        password=m.hexdigest(),
        num="0789101162",
        firstname="Nami",
        lastname="LOL",
        email="mugiwara.nami@gmail.com",
        town="Mont Corvo",
        postal_code="45000",
        street="5 rue du roi des voleurs",
        profile_picture="https://eu.ui-avatars.com/api/?name=user2",
        is_admin=False)
    to_import.append(user2)

    m = sha256()
    m.update("user3".encode())
    user3 = USER(
        username="user3",
        password=m.hexdigest(),
        num="0789101162",
        firstname="Nice",
        lastname="Guy",
        email="oicegenerator@gmail.com",
        town="Mont Corvo",
        postal_code="45000",
        street="69 rue des 420",
        profile_picture="https://eu.ui-avatars.com/api/?name=user3",
        is_admin=False)

    to_import.append(user3)
    # création de messages
    t1 = TICKET(1, "ticket message 1", 0, to_import[1])
    to_import.append(t1)
    to_import.append(MESSAGE(

        is_admin_message=0,
        datetime_message=datetime.datetime(2017, 11, 28, 23, 55, 59, 342380),
        content_message="Bonjour de la par d'un admin",
        ticket=t1))

    to_import.append(MESSAGE(
        is_admin_message=1,
        datetime_message=datetime.datetime(2017, 11, 28, 23, 56, 59, 342380),
        content_message="Salut je suis un admin",
        ticket=t1))

    to_import.append(MESSAGE(
        is_admin_message=0,
        datetime_message=datetime.datetime(2017, 11, 28, 23, 57, 59, 342380),
        content_message="OK pouvez vous m'aider ?",
        ticket=t1))

    t2 = TICKET(2, "ticket message 2", 0, to_import[2])
    to_import.append(t2)
    to_import.append(MESSAGE(

        is_admin_message=1,
        datetime_message=datetime.datetime(2015, 8, 23, 10, 55, 9, 342380),
        content_message="Salut bro",
        ticket=t2))

    t3 = TICKET(3, "ticket message 3", 1, to_import[0])
    to_import.append(t3)
    to_import.append(MESSAGE(

        is_admin_message=0,
        datetime_message=datetime.datetime(2021, 11, 22, 14, 12, 8, 300080),
        content_message="Test message, ceci est un message test",
        ticket=t3))

    t4 = TICKET(4, "ticket message 4", 1, to_import[3])
    to_import.append(t4)
    to_import.append(MESSAGE(

        is_admin_message=1,
        datetime_message=datetime.datetime(2020, 12, 31, 23, 59, 59, 300080),
        content_message="Bonne année 2021",
        ticket=t4))

    t5 = TICKET(5, "ticket message 4", 1, to_import[4])
    to_import.append(t5)
    to_import.append(MESSAGE(
                             is_admin_message=1,
                             datetime_message=datetime.datetime(1989, 9, 30, 23, 59, 59, 300080),
                             content_message="Wtf les mecs je viens d'inventé internet",
                             ticket=t5))

    device1 = DEVICE(
        num_device="0769342048",
        name_device="JuleBrossier",
        row_parameters_device="",
        user=user1,

    )

    device2 = DEVICE(
        num_device="0781546427",
        name_device="DorianHardy",
        row_parameters_device="",
        user=user2,

    )

    device3 = DEVICE(
        num_device="0664277796",
        name_device="Andrew",
        row_parameters_device="",
        user=user3,

    )
    to_import.append(device1)
    to_import.append(device2)
    to_import.append(device3)

    for obj in track(to_import):
        db.session.add(obj)

    db.session.commit()
