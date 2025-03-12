import random
from typing import Tuple

from .base import Automaton

class BriansBrain(Automaton):
    def __init__(self, file_path: str = None, grid_dims: Tuple[int, int] = (200, 100), cell_size: int = 8, frame_rate: int = 30):
        super().__init__('Brian\'s Brain', file_path, grid_dims, cell_size, frame_rate)
        self.run_simulation()
    
    def init_grid(self, grid_dims: Tuple[int, int]) -> None:
        self.grid = [[random.choice([0, 1, 2]) for _ in range(grid_dims[1])] for _ in range(grid_dims[0])]
    
    def next_generation(self) -> None:
        new_grid = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        
        for x, y in self.get_grid():
            adjacent = self.count_adjacent(x, y)
            # Dead cell with 2 live neighbors becomes live
            if self.grid[x][y] == 0 and adjacent == 2:
                new_grid[x][y] = 1
            # Live cell with 2 live neighbors remains live
            elif self.grid[x][y] == 1:
                new_grid[x][y] = 2
            # Live cell with 1 or 0 live neighbors dies
            elif self.grid[x][y] == 2:
                new_grid[x][y] = 0

        self.grid = new_grid
