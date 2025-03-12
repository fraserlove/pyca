import random
from typing import Tuple

from .base import Automaton

class PredatorPrey(Automaton):
    def __init__(self, file_path: str = None, grid_dims: Tuple[int, int] = (200, 100), cell_size: int = 8, frame_rate: int = 30):
        super().__init__('Predator and Prey', file_path, grid_dims, cell_size, frame_rate)
        self.p_prey = 0.5
        self.p_pred = 0.4
        self.run_simulation()

    def init_grid(self, grid_dims: Tuple[int, int]) -> None:
        self.grid = [[random.choice([0, 1, 2]) for _ in range(grid_dims[1])] for _ in range(grid_dims[0])]

    def next_generation(self) -> None:
        new_grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]

        # Prey disperse
        for x, y in self.get_grid():
            # Keep prey in place if it exists
            if self.grid[x][y] == 1:
                new_grid[x][y] = 1
                # Try to reproduce into empty adjacent cells
                for nx, ny in self.get_adjacent(x, y):
                    if self.grid[nx][ny] == 0 and random.uniform(0, 1) < self.p_prey:
                        new_grid[nx][ny] = 1

        # Predator disperse
        for x, y in self.get_grid():
            # Keep predator in place if it exists
            if self.grid[x][y] == 2:
                new_grid[x][y] = 2
                # Try to infect adjacent prey
                for nx, ny in self.get_adjacent(x, y):
                    if self.grid[nx][ny] == 1 and random.uniform(0, 1) < self.p_pred:
                        new_grid[nx][ny] = 2

        # Remove predators that are isolated (no adjacent prey)
        for x, y in self.get_grid():
            if new_grid[x][y] == 2:
                prey_adjacent = False
                for nx, ny in self.get_adjacent(x, y):
                    if new_grid[nx][ny] == 1:
                        prey_adjacent = True
                        break
                if not prey_adjacent:
                    new_grid[x][y] = 0

        self.grid = new_grid
