import click
from .app import app, db
from rich.console import Console
from rich.progress import track
import datetime
from .models import USER, MESSAGE, TICKET


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
    # création de deux admins

    to_import.append(USER("admin",
                          "admin",
                          "0781546427",
                          "John",
                          "Doe",
                          "johndoe@gmail.com",
                          "Bourges",
                          "18110",
                          "167",
                          "profile_picture_user",
                          0))
    to_import.append(USER("admin2",
                          "admin2",
                          "0654321012",
                          "Michel",
                          "Dupon",
                          "micheldupon@gmail.com",
                          "Lille",
                          "59350",
                          "48 rue des coquelicots",
                          "profile_picture_user",
                          0))

    # création de 3 users
    to_import.append(USER("user1",
                          "user1",
                          "0789101112",
                          "Luffy",
                          "Monkey D",
                          "mugiwara@gmail.com",
                          "Mont Corvo",
                          "45000",
                          "5 rue du roi des pirates",
                          "profile_picture_user",
                          1))
    to_import.append(USER("user2",
                          "user2",
                          "0769696969",
                          "Emma",
                          "Brancourt",
                          "emmabrancourt@gmail.com",
                          "Tours",
                          "37000",
                          "42 rue de la vérité",
                          "profile_picture_user",
                          1))
    to_import.append(USER("user3",
                          "user3",
                          "6942069420",
                          "Nice",
                          "Guy",
                          "noicegenerator@gmail.com",
                          "Nice",
                          "06000",
                          "69 rue des 420",
                          "profile_picture_user",
                          1))

    # création de messages
    t1 = TICKET(1, "ticket message 1", 0, to_import[1])
    to_import.append(t1)
    to_import.append(MESSAGE(1,
                             0,
                             datetime.datetime(2017, 11, 28, 23, 55, 59, 342380),
                             "Bonjour de la par d'un admin",
                             t1))

    t2 = TICKET(2, "ticket message 2", 0, to_import[2])
    to_import.append(t2)
    to_import.append(MESSAGE(2,
                             1,
                             datetime.datetime(2015, 8, 23, 10, 55, 9, 342380),
                             "Salut bro",
                             t2))

    t3 = TICKET(3, "ticket message 3", 1, to_import[0])
    to_import.append(t3)
    to_import.append(MESSAGE(3,
                             0,
                             datetime.datetime(2021, 11, 22, 14, 12, 8, 300080),
                             "Test message, ceci est un message test",
                             t3))

    t4 = TICKET(4, "ticket message 4", 1, to_import[3])
    to_import.append(t4)
    to_import.append(MESSAGE(4,
                             1,
                             datetime.datetime(2020, 12, 31, 23, 59, 59, 300080),
                             "Bonne année 2021",
                             t4))

    t5 = TICKET(5, "ticket message 4", 1, to_import[4])
    to_import.append(t5)
    to_import.append(MESSAGE(5,
                             1,
                             datetime.datetime(1989, 9, 31, 23, 59, 59, 300080),
                             "Wtf les mecs je viens d'inventé internet",
                             t5))

    for obj in track(to_import):
        db.session.add(obj)

    db.session.commit()
