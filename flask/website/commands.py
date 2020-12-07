import click
from .app import app, db


@app.cli.command()
@click.argument('create')
def load_db(create):
    pass
