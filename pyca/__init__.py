import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

__version__ = '0.1.0'

from .automata import Automaton, BriansBrain, GameOfLife, LangtonsAnt, PredatorPrey, WireWorld

__all__ = ['Automaton', 'BriansBrain', 'GameOfLife', 'LangtonsAnt', 'PredatorPrey', 'WireWorld']
