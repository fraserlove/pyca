import typer
from typing import Optional
from pathlib import Path

from pyca import __version__
from pyca.automata import *

app = typer.Typer()

AUTOMATA = {
    'game_of_life': GameOfLife,
    'langtons_ant': LangtonsAnt,
    'predator_prey': PredatorPrey,
    'brians_brain': BriansBrain,
    'wire_world': WireWorld
}

DEFAULT_GRID_SIZE = (200, 100)
DEFAULT_CELL_SIZE = 10
DEFAULT_FRAME_RATE = 30

def version_callback(value: bool) -> None:
    if value:
        print(f'{__package__} {__version__}')
        raise typer.Exit()

def list_callback(value: bool) -> None:
    if value:
        typer.echo("Available automata: " + ", ".join(AUTOMATA.keys()))
        raise typer.Exit()

@app.command()
def main(
    automaton: str = typer.Argument(..., help='Path to automaton file or type of automaton to run.'),
    width: int = typer.Option(DEFAULT_GRID_SIZE[0], '--width', '-w', help='Grid width.'),
    height: int = typer.Option(DEFAULT_GRID_SIZE[1], '--height', '-h', help='Grid height.'),
    cell_size: int = typer.Option(DEFAULT_CELL_SIZE, '--cell-size', '-c', help='Size of each cell in pixels.'),
    frame_rate: int = typer.Option(DEFAULT_FRAME_RATE, '--frame-rate', '-r', help='Frame rate of simulation.'),
    version: bool = typer.Option(False, '--version', '-v', callback=version_callback, help='Show version information.'),
    list: bool = typer.Option(False, '--list', '-l', callback=list_callback, help='List available automata.')
):
    # Check if the argument is a file path
    if Path(automaton).exists():
        try:
            simulation = Automaton.from_file(
                automaton,
                cell_size=cell_size,
                frame_rate=frame_rate
            )
            return
        except Exception as e:
            typer.echo(f'Error loading {automaton}: {e}')
            raise typer.Exit(1)

    # If not a file, treat as automaton type
    if automaton not in AUTOMATA:
        available = ', '.join(AUTOMATA.keys())
        typer.echo(f'Error: Unknown automaton \'{automaton}\'. Available options: {available}')
        raise typer.Exit(1)

    grid_dims = (width, height)
    automaton_class = AUTOMATA[automaton]
    
    simulation = automaton_class(
        grid_dims=grid_dims,
        cell_size=cell_size,
        frame_rate=frame_rate
    )

def run():
    app()