from .base import Parser
from .rle import RLEParser

__all__ = ['RLEParser']

parsers = {
    'rle': RLEParser
}

def find_parser(file_path: str) -> Parser | None:
    '''
    Finds and returns the parser for the given file path.
    '''
    file_extension = file_path.split('.')[-1]
    if file_extension in parsers:
        return parsers[file_extension]()
    else:
        raise ValueError(f'Unsupported file type: {file_path}')