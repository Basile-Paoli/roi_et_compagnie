
from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable, Literal, Optional

from game.dice import DieResult


class KingdomCard(ABC):

    @abstractmethod
    def value(self, kingdom: Iterable["KingdomCard"]) -> int:
        pass


class LocationType(Enum):
    CITY = 0
    MINE = 1
    WORKSHOP = 2
    ORCS_VILLAGE = 3
    FOREST = 4


class Location(KingdomCard):

    def __init__(self, value: Literal[2, 3, 4] , location_type: LocationType):
        self._value = value
        self.location_type = location_type

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value


def get_initial_locations():
    return list(
        [
            Location(4, t),
            Location(3, t),
            Location(2, t),
        ]
        for t in LocationType
    )


class Inhabitant(KingdomCard, ABC):

    @property
    @abstractmethod
    def related_location(self) -> Optional[LocationType]:
        pass

    @abstractmethod
    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        pass

    @abstractmethod
    def can_take(self, dice: Iterable[DieResult]) -> bool:
        pass


class Penalty(int):

    def value(self, kingdom: Iterable[object]) -> int:
        return -self


def initial_penalties() -> list[Penalty]:
    return [Penalty(i) for i in ([1] * 4 + [2] * 3 + [3] * 2 + [4] * 1)]
