import numpy as np

class Parser:
    def __init__(self):
        self.grid = np.array([], dtype=np.int8)
    
    def load(self, file_path: str) -> np.ndarray:
        '''
        Parses the grid from the file.
        '''
        raise NotImplementedError('Subclasses must implement load()')
    
    def pad(self, pad_width: int = 1) -> np.ndarray:
        '''
        Pads the grid with a border of zeros.
        '''
        self.grid = np.pad(self.grid, pad_width=pad_width, mode='constant', constant_values=0)
        return self.grid