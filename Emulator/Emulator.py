from rich.console import Console
from rich.table import Table
from protocols.AlertProtocol import *
from protocols.ParkmodeProtocol import *
from protocols.RideProtocol import *

console = Console()


def welcome(protocols):
    table = Table(title="BiKeeper")
    table.add_column("BiKeeper SMS Emulator", style="magenta", width=90)
    table.add_row("Welcome to SMS Emulator !  ")
    table.add_row("You can :")
    table.add_row("- Generate Random message")
    table.add_row("- List protocols available")
    table.add_row("To see the help add this arg : --help ")
    table.columns[0].header_style = "bold green"
    console.print(table)


class Emulator:

    def __init__(self, options, protocols):
        self.protocol = options
        self.available_protocols = protocols

    def start(self):
        welcome(self.available_protocols)
        self.generate()

    def alert(self):
        a = AlertProtocol()

    def ride(self):
        r = RideProtocol()

    def parkmode(self):
        p = ParkmodeProtocol()

    def generate(self):
        console.print("Starting generator ...")

        protocols_table = {"alert": self.alert(),
                           "ride": self.ride(),
                           "park": self.parkmode()}

        protocols_table.get(self.protocol, "Invalid protocols")
