from abc import ABC, abstractmethod
from typing import Iterable

from game.dice import DiceColor, Die 
from game.location import LocationType


class Inhabitant(ABC):
    def __init__(self, color: LocationType) -> None:
        self.color = color

    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @abstractmethod
    def can_take(self, dice: Iterable[Die]) -> bool:
        pass


class Gnome(Inhabitant):
    def __init__(self, color: LocationType, dice_color: DiceColor, dice_count: int) -> None:
        super().__init__(color)
        self.dice_color = dice_color
        self.dice_count = dice_count

    @property
    def value(self) -> int:
        return 8

    def can_take(self, dice: Iterable[Die]) -> bool:
        return sum(1 for die in dice if die[1] == self.dice_color) >= self.dice_count
