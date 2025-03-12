import time
import pygame
from typing import Generator, Tuple

from ..parsers import find_parser

class Automaton:
    def __init__(self, name: str, file_path: str = None, grid_dims: Tuple[int, int] = None, cell_size: int = None, frame_rate: int = None):
        self.cell_size = cell_size
        self.frame_rate = frame_rate
        self.paused = False

        if file_path:
            self.import_grid(file_path)
        else:
            self.init_grid(grid_dims)
        
        pygame.init()
        self.display = pygame.display.set_mode((len(self.grid) * self.cell_size, len(self.grid[0]) * self.cell_size))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(name)
    
    def init_grid(self, grid_dims: Tuple[int, int]) -> None:
        self.grid = [[0 for _ in range(grid_dims[1])] for _ in range(grid_dims[0])]
    
    def import_grid(self, file_path: str) -> None:
        parser = find_parser(file_path)
        self.grid = parser.load(file_path)

    def next_generation(self) -> None:
        raise NotImplementedError('Subclasses must implement next_generation()')
    
    def get_grid(self) -> Generator[Tuple[int, int], None, None]:
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                yield x, y
    
    def get_adjacent(self, x: int, y: int) -> Generator[Tuple[int, int], None, None]:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                yield nx % len(self.grid), ny % len(self.grid[0])
    
    def count_adjacent(self, x: int, y: int, value: int = 1) -> int:
        return sum(self.grid[nx][ny] == value for nx, ny in self.get_adjacent(x, y))
    
    def draw_grid(self) -> None:
        self.display.fill(pygame.Color('black'))
        for x, y in self.get_grid():
            if self.grid[x][y] == 1:
                pygame.draw.rect(self.display, (255, 255, 255), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
            elif self.grid[x][y] == 2:
                pygame.draw.rect(self.display, (128, 128, 128), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()
    
    def run_simulation(self) -> None:
        x = 0
        while True:
            if self.frame_rate:
                self.clock.tick(self.frame_rate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_RIGHT and self.paused:
                        # Advance one step when right arrow is pressed while paused
                        self.next_generation()
                        self.draw_grid()
            pygame.image.save(self.display, f'examples/images/gif/{self.__class__.__name__}_{x:04}.png')
            x += 1
            
            self.draw_grid()
            
            if not self.paused:
                self.next_generation()

    @classmethod
    def from_file(cls, file_path: str, cell_size: int = 8, frame_rate: int = 30) -> 'Automaton':
        """Factory method to create the appropriate automaton from an RLE file"""
        parser = find_parser(file_path)
        grid = parser.load(file_path)
        
        # Get the automaton type from the parser
        if not hasattr(parser, 'automaton') or not parser.automaton:
            raise ValueError('RLE file must specify automaton type in header')
            
        # Import all automaton classes
        from . import GameOfLife, BriansBrain, LangtonsAnt, PredatorPrey, WireWorld
        
        # Map automaton names to classes
        automaton_map = {}
        for name, cls in locals().items():
            if isinstance(cls, type) and issubclass(cls, Automaton) and cls != Automaton:
                # Convert CamelCase to snake_case
                snake_case = ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
                automaton_map[snake_case] = cls
        
        # Get the appropriate automaton class
        automaton_class = automaton_map.get(parser.automaton)
        if not automaton_class:
            raise ValueError(f'Unknown automaton type: {parser.automaton}')
            
        # Create and return the automaton instance
        return automaton_class(file_path=file_path, cell_size=cell_size, frame_rate=frame_rate)