from enum import Enum


class Tile(Enum):

    EMPTY = 0

    BLACK = 1

    WHITE = 2

    BLACK_POINT =3 

    WHITE_POINT = 4

    BORDER = 5

    TEMP_ONE = 6
    
    TEMP_ZERO = 7
    
    TEMP_OPPOSITE_ONE = 8
    
    TEMP_OPPOSITE_ZERO = 9
    
    WHITE_DEAD = 10
    
    BLACK_DEAD = 11


class CheckPointResult(Enum):

    FALSE = 0

    TRUE = 1

    BIG_FALSE = 2