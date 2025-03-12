import random
from typing import Tuple

from .base import Automaton

class GameOfLife(Automaton):
    def __init__(self, file_path: str = None, grid_dims: Tuple[int, int] = (200, 100), cell_size: int = 8, frame_rate: int = 30):
        super().__init__('Game of Life', file_path, grid_dims, cell_size, frame_rate)
        self.run_simulation()
    
    def init_grid(self, grid_dims: Tuple[int, int]) -> None:
        self.grid = [[random.choice([0, 1]) for _ in range(grid_dims[1])] for _ in range(grid_dims[0])]
    
    def next_generation(self) -> None:
        new_grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        
        for x, y in self.get_grid():
            adjacent = self.count_adjacent(x, y)
            # Live cell with 2 or 3 live neighbors remains live
            if self.grid[x][y] == 1 and adjacent in [2, 3]:
                new_grid[x][y] = 1
            # Dead cell with 3 live neighbors becomes live
            elif self.grid[x][y] == 0 and adjacent == 3:
                new_grid[x][y] = 1
                        
        self.grid = new_grid
