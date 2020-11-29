from rich.console import Console
from rich import print
from rich.progress import track
from rich.table import Column, Table
import time
import click
from rich.columns import Columns
from rich.panel import Panel
import json
from Emulator import *

protocols_list = [
    {"TYPE-alert": "Alert protocol to send alert"},
    {"TYPE-parkmode": "Message sent when BiKeeper is parked"},
    {"TYPE-ride": "Message sent during a ride"}
]

json_protocols_format = json.dumps(protocols_list)

console = Console()


def get_content(user):
    """Extract text from user dict."""
    title = str(list(user.keys())[0])
    content = user[title]
    return f"[b]{title}[/b]\n[yellow]{content}"


@click.command()
@click.option('--list-protocols', is_flag=True, help="Will list the protocols.")
@click.option('--gen', help='Generate fake message')
def cli(list_protocols, gen):
    if list_protocols:
        users = json.loads(json_protocols_format)
        user_renderables = [Panel(get_content(user), expand=True) for user in users]
        console.print(Columns(user_renderables))

    if gen:
        emu = Emulator(gen, protocols_list)
        emu.start()


cli()
