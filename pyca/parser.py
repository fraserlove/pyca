import re
import numpy as np

class Parser:
    def __init__(self):
        self.grid = None
        self.automaton = None
        
    def load(self, file_path: str) -> np.ndarray:
        '''
        Parses a cellular automaton grid from a .ca file.
        '''
        with open(file_path, 'r') as f:
            lines = f.readlines()

        if not file_path.endswith('.ca'):
            raise ValueError('Unsupported file type.')
        
        header_found = False
        pattern_lines = []
        header_params = {'w': 0, 'h': 0, 'x': 0, 'y': 0}
        
        for line in lines:
            line = line.strip()
            
            # Skip blank lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Process header
            if line.startswith('w ') or line.startswith('w='):
                self._parse_header(line, header_params)
                header_found = True
                continue
                
            # Collect pattern data
            if header_found:
                pattern_lines.append(line.replace(' ', '').rstrip('!'))
        
        # Parse the pattern data
        self._parse_pattern_data(''.join(pattern_lines), header_params)
        
        return self.grid
    
    def _parse_header(self, line: str, header_params: dict) -> None:
        '''
        Parses the header line to extract parameters.
        '''
        params = {
            'width': r'w\s*=\s*(\d+)',
            'height': r'h\s*=\s*(\d+)',
            'x': r'x\s*=\s*(-?\d+)',
            'y': r'y\s*=\s*(-?\d+)',
            'automaton': r'automaton\s*=\s*(\w+)'
        }
        
        for param, pattern in params.items():
            match = re.search(pattern, line)
            if match:
                value = match.group(1)
                if param != 'automaton':
                    header_params[param] = int(value)
                else:
                    self.automaton = value
                    
    def _parse_pattern_data(self, pattern_data: str, header_params: dict) -> None:
        '''
        Parses the RLE pattern data to create the grid.
        '''
        rows = []
        current_row = []
        run_count = ''
        
        for char in pattern_data:
            if char.isdigit():
                run_count += char
            else:
                count = int(run_count) if run_count else 1
                run_count = ''
                
                if char == '$':
                    # End of row
                    rows.append(current_row)
                    # Add empty rows if count > 1
                    rows.extend([[] for _ in range(count - 1)])
                    current_row = []
                elif char == '.':
                    # Empty cell (state 0)
                    current_row.extend([0] * count)
                elif 'A' <= char <= 'Z':
                    # States 1-26 (A=1, B=2, etc.)
                    state = ord(char) - ord('A') + 1
                    current_row.extend([state] * count)
        
        # Add the last row if not empty
        if current_row:
            rows.append(current_row)
        
        self._transform_grid(rows, header_params)
    
    def _transform_grid(self, rows, header_params):
        '''
        Create the final grid with proper dimensions and pattern placement.
        '''
        
        # Get pattern dimensions
        pattern_height = len(rows)
        pattern_width = max(len(row) for row in rows) if rows else 0

        # Use header dimensions or pattern dimensions
        height = header_params['height'] if header_params['height'] > 0 else pattern_height
        width = header_params['width'] if header_params['width'] > 0 else pattern_width
        
        self.grid = np.zeros((width, height), dtype=np.int8)
        
        # Calculate offsets to center the pattern and apply the x,y offset
        x_offset = (width - pattern_width) // 2 + header_params['x']
        y_offset = (height - pattern_height) // 2 + header_params['y']
        
        # Check if pattern will be partially out of bounds
        if not (0 <= x_offset <= width - pattern_width and 0 <= y_offset <= height - pattern_height):
            print('Warning: Pattern wrapping around grid boundaries due to offset values.')
        
        # Fill the grid with the pattern data
        for y, row in enumerate(rows):
            for x, cell in enumerate(row):
                grid_x = (x + x_offset) % width
                grid_y = (y + y_offset) % height
                self.grid[grid_x, grid_y] = cell