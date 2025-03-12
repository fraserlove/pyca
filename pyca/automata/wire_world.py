import random
import pygame
from typing import Tuple

from .base import Automaton

class WireWorld(Automaton):
    def __init__(self, file_path: str = None, grid_dims: Tuple[int, int] = (200, 100), cell_size: int = 8, frame_rate: int = 30):
        super().__init__('Wire World', file_path, grid_dims, cell_size, frame_rate)
        self.run_simulation()

    def init_grid(self, grid_dims: Tuple[int, int]) -> None:
        raise NotImplementedError('Wire World does not support randomised grids')

    def next_generation(self) -> None:
        new_grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]

        # Electron moves forward
        for x, y in self.get_grid():
            if self.grid[x][y] == 3:
                new_grid[x][y] = 3
                adjacent = self.count_adjacent(x, y, 1)
                if adjacent in [1, 2]:
                    new_grid[x][y] = 1
            elif self.grid[x][y] == 1:
                new_grid[x][y] = 2
            elif self.grid[x][y] == 2:
                new_grid[x][y] = 3

        self.grid = new_grid

    def draw_grid(self) -> None:
        self.display.fill(pygame.Color('black'))
        for x, y in self.get_grid():
            if self.grid[x][y] == 3:
                pygame.draw.rect(self.display, (230, 239, 62), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
            elif self.grid[x][y] == 1:
                pygame.draw.rect(self.display, (62, 174, 239), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
            elif self.grid[x][y] == 2:
                pygame.draw.rect(self.display, (239, 62, 62), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.update()
