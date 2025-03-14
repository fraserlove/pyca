# PyCA

PyCA is a Python package and command line tool for running cellular automata simulations. Currently PyCA supports Conway's Game of Life, Langton's Ant, Predator Prey, Brian's Brain, and Wire World. PyCA is built on top of Pygame and is designed to be easy to use and extend.

Notably PyCA allows for cellular automata to be described in `.ca` format, which is a simple format for describing patterns in cellular automata using RLE. If no `.ca` file is provided PyCA will generate a randomised initial state. PyCA also allows for the creation of custom cellular automata by subclassing the base `Automaton` class.

## Installation and Usage

Before installing PyCA, consider using a virtual environment for the installation to avoid conflicts with other Python packages.

```sh
python -m venv .venv
source .venv/bin/activate
```

Clone the repository and install the package.

```sh
git clone https://github.com/fraserlove/pyca.git
cd pyca
pip install .
```

Verify that `pyca` was installed successfully via `pyca --version`.

Shell completion is available for your shell and can be viewed with `pyca --show-completion` or installed with `pyca --install-completion`.

The PyCA command line tool can be used to run cellular automata simulations. PyCA will generate a randomised initial state if no `.ca` file is provided. To run a cellular automaton from an `.ca` file, use the following command:

```sh
pyca AUTOMATON [OPTIONS]
```
where `AUTOMATON` is the name of the automaton to run (e.g. `game_of_life`) or the path to an `.ca` file (e.g. `grids/game_of_life/pyca.ca`). Options can be viewed with `pyca --help`.

### Custom Grids

To run a cellular automaton from an `.ca` file, use the following command:

```sh
pyca grids/game_of_life/pyca.ca
```

In order for PyCA to know which automaton to use, the `.ca` file must contain an `automaton` field in the header.

Note that the grid is wrapped by default, so a layer of padding is suggested around all `.ca` files to ensure that interactions between the edges of the automaton are handled correctly.

### Importing PyCA

To use PyCA in a module, import the relevant automaton class from the `pyca` package.

```python
from pyca import GameOfLife

# Create and run a randomised instance of Conway's Game of Life
GameOfLife(grid_dims=(200, 100), cell_size=10, frame_rate=30)

# Create and run a instance of Conway's Game of Life from a file
GameOfLife('grids/game_of_life/pyca.ca')
```
PyCA supports the creation of custom cellular automata by subclassing the base `Automaton` class.

### Controls

`SPACE` key toggles pause/play.
`RIGHT ARROW` key advances one generation when paused.
`ESC` key quits the simulation.

## Examples

![Wire World](assets/wire_world.png)

![Predator Prey](assets/predator_prey.png)

![Brian's Brain](assets/brians_brain.png)

![Langton's Ant](assets/langtons_ant.png)

![Conway's Game of Life](assets/game_of_life.png)
