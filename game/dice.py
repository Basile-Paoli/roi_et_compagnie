import random
from typing import Literal, Iterable, Any
from enum import Enum

type DiceValue = Literal[1, 2, 3, 4, 5, 6]


class DiceColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    def to_json(self) -> int:
        return self.value

    @staticmethod
    def from_json(value: int) -> "DiceColor":
        return DiceColor(int(value)) if int(value) in (1, 2, 3) else DiceColor.RED  # Default to RED if invalid


type DieResult = tuple[DiceValue, DiceColor]


class Die(list[DieResult]):

    def __init__(self, die: Iterable[DieResult]):
        super().__init__(die)
        self.currentResult: DieResult = random.choice(self)

    def roll(self) -> DieResult:
        self.currentResult = random.choice(self)
        return self.currentResult

    def to_json(self) -> dict[Any, Any]:
        return {
            "currentResult": self.currentResult,
            "die": list(self)
        }

    @staticmethod
    def from_json(data: dict[Any, Any]) -> "Die":
        die = Die(((side[0], DiceColor.from_json(side[1])) for side in data["die"]))
        die.currentResult = (data["currentResult"][0], DiceColor.from_json(data["currentResult"][1]))
        return die


def die1(): return Die([
    (1, DiceColor.BLUE),
    (2, DiceColor.GREEN),
    (3, DiceColor.RED),
    (4, DiceColor.RED),
    (5, DiceColor.GREEN),
    (6, DiceColor.BLUE)
])


def die2(): return Die([
    (1, DiceColor.RED),
    (2, DiceColor.BLUE),
    (3, DiceColor.GREEN),
    (4, DiceColor.GREEN),
    (5, DiceColor.BLUE),
    (6, DiceColor.RED)
])


def die3(): return Die([
    (1, DiceColor.GREEN),
    (2, DiceColor.RED),
    (3, DiceColor.BLUE),
    (4, DiceColor.BLUE),
    (5, DiceColor.RED),
    (6, DiceColor.GREEN)
])


def get_dice(): return [die1(), die1(), die2(), die2(), die3(), die3()]
