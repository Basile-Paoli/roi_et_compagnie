from typing import  Literal
from enum import Enum

type DiceValue = Literal[1, 2, 3, 4, 5, 6]


class DiceColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


type DieResult = tuple[DiceValue, DiceColor]

class Die(list[DieResult]):
    pass



die1 = Die([
    (1, DiceColor.BLUE),
    (2, DiceColor.GREEN),
    (3, DiceColor.RED),
    (4, DiceColor.RED),
    (5, DiceColor.GREEN),
    (6, DiceColor.BLUE)
])

die2 = Die([
    (1, DiceColor.RED),
    (2, DiceColor.BLUE),
    (3, DiceColor.GREEN),
    (4, DiceColor.GREEN),
    (5, DiceColor.BLUE),
    (6, DiceColor.RED)
])

die3 = Die([
    (1, DiceColor.GREEN),
    (2, DiceColor.RED),
    (3, DiceColor.BLUE),
    (4, DiceColor.BLUE),
    (5, DiceColor.RED),
    (6, DiceColor.GREEN)
])

dice = [die1, die2, die3] * 2