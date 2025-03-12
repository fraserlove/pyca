from typing import Tuple

from .base import Automaton

class LangtonsAnt(Automaton):
    def __init__(self, file_path: str = None, grid_dims: Tuple[int, int] = (200, 100), cell_size: int = 8, frame_rate: int = None):
        super().__init__('Langton\'s Ant', file_path, grid_dims, cell_size, frame_rate)
        self.forward = [0, -1]
        self.x, self.y = grid_dims[0] // 2, grid_dims[1] // 2
        self.run_simulation()

    def next_generation(self) -> None:
        # Turn right if on black square, left if on white square
        if self.grid[self.x][self.y] == 1:
            self.forward = [-self.forward[1], self.forward[0]]
            self.grid[self.x][self.y] = 0
        else:
            self.forward = [self.forward[1], -self.forward[0]]
            self.grid[self.x][self.y] = 1

        # Move forward
        dx, dy = self.forward
        self.x = (self.x + dx) % len(self.grid)
        self.y = (self.y + dy) % len(self.grid[0])
