from typing import  Literal
from enum import Enum

type DiceValue = Literal[1, 2, 3, 4, 5, 6]


class DiceColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


type DieResult = tuple[DiceValue, DiceColor]
