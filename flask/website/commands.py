import click
from .app import app, db
from rich.console import Console
from rich.progress import track
import time
from .models import USER


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

    for obj in track(to_import):
        db.session.add(obj)

    db.session.commit()
