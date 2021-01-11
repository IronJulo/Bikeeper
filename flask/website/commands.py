import click
from .app import app, db
from rich.progress import track
from rich.console import Console
import time


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


