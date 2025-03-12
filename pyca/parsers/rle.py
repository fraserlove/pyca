import re
import numpy as np

from .base import Parser

class RLEParser(Parser):
    def __init__(self):
        super().__init__()
        self.width = 0
        self.height = 0
        self.x = 0
        self.y = 0
        self.automaton = None
        
    def load(self, file_path: str) -> np.ndarray:
        '''
        Parses the grid from an RLE file.
        
        RLE (Run Length Encoded) is a format used by Golly and other cellular automata
        simulators to store patterns efficiently.
        '''
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Process header and comments
        header_found = False
        pattern_lines = []
        comments = []
        
        for line in lines:
            line = line.strip()
            
            # Skip blank lines
            if not line:
                continue
                
            # Process comments
            if line.startswith('#'):
                comments.append(line)
                continue
                
            # Process header (w = width, h = height, x = x, y = y)
            if line.startswith('w ') or line.startswith('w='):
                self._parse_header(line)
                header_found = True
                continue
                
            # Process pattern data
            if header_found:
                pattern_lines.append(line.replace(' ', ''))
        
        # Join all pattern lines
        pattern_data = ''.join(pattern_lines)
        
        # Parse the pattern data
        self._parse_pattern_data(pattern_data)
        
        return self.grid
    
    def _parse_header(self, line: str) -> None:
        '''Parse the RLE header line'''
        # Extract width
        width_match = re.search(r'w\s*=\s*(\d+)', line)
        if width_match:
            self.width = int(width_match.group(1))
            
        # Extract height
        height_match = re.search(r'h\s*=\s*(\d+)', line)
        if height_match:
            self.height = int(height_match.group(1))

        # Extract x
        x_match = re.search(r'x\s*=\s*(-?\d+)', line)
        if x_match:
            self.x = int(x_match.group(1))

        # Extract y
        y_match = re.search(r'y\s*=\s*(-?\d+)', line)
        if y_match:
            self.y = int(y_match.group(1))
            
        # Extract automaton
        automaton_match = re.search(r'automaton\s*=\s*(\w+)', line)
        if automaton_match:
            self.automaton = automaton_match.group(1)
    
    def _parse_pattern_data(self, pattern_data: str) -> None:
        '''Parse the RLE pattern data and create the grid'''
        # Remove the trailing '!' if present
        if pattern_data.endswith('!'):
            pattern_data = pattern_data[:-1]
        
        rows = []
        current_row = []
        run_count = ""
        
        for char in pattern_data:
            if char.isdigit():
                run_count += char
            elif char == '$':
                # End of row
                rows.append(current_row)
                # Add empty rows if run_count > 1
                count = int(run_count) if run_count else 1
                for _ in range(count - 1):
                    rows.append([])
                current_row = []
                run_count = ""
            elif char in 'b.':
                # Dead cell (state 0)
                count = int(run_count) if run_count else 1
                current_row.extend([0] * count)
                run_count = ""
            elif char == 'A' or char == 'o':
                # Alive cell (state 1)
                count = int(run_count) if run_count else 1
                current_row.extend([1] * count)
                run_count = ""
            elif 'B' <= char <= 'X':
                # States 2-24
                count = int(run_count) if run_count else 1
                state = ord(char) - ord('A') + 1
                current_row.extend([state] * count)
                run_count = ""
            elif char == 'p' and pattern_data.find(char) < len(pattern_data) - 1:
                # States 25-48 (pA-pX)
                next_char = pattern_data[pattern_data.find(char) + 1]
                if 'A' <= next_char <= 'X':
                    count = int(run_count) if run_count else 1
                    state = 24 + (ord(next_char) - ord('A') + 1)
                    current_row.extend([state] * count)
                run_count = ""
            # Additional state ranges (q-y) could be implemented similarly
        
        # Add the last row if not empty
        if current_row:
            rows.append(current_row)
        
        # Create the grid with the dimensions specified in the header
        # If header dimensions are not provided, use the actual pattern dimensions
        pattern_height = len(rows)
        pattern_width = max([len(row) for row in rows] or [0])
        
        self._transform_grid(rows, pattern_width, pattern_height)
    
    def _transform_grid(self, rows, pattern_width, pattern_height):
        '''Apply resizing and offsetting to the grid based on header information'''
        
        # Use header dimensions for the full grid size
        height = self.height if self.height > 0 else pattern_height
        width = self.width if self.width > 0 else pattern_width
        
        self.grid = np.zeros((width, height), dtype=np.int8)
        
        # Calculate offsets to center the pattern and apply the x,y offset
        x_offset = (width - pattern_width) // 2 + self.x
        y_offset = (height - pattern_height) // 2 + self.y
        
        # Check if pattern will be partially out of bounds
        if x_offset < 0 or y_offset < 0 or x_offset + pattern_width > width or y_offset + pattern_height > height:
            print('Warning: Pattern wrapping around grid boundaries due to offset values. May cause unexpected behavior.')
        
        # Fill the grid with the pattern data at the calculated position
        for y, row in enumerate(rows):
            for x, cell in enumerate(row):
                grid_x = (x + x_offset) % width  # Wrap around the grid
                grid_y = (y + y_offset) % height  # Wrap around the grid
                self.grid[grid_x, grid_y] = cell
