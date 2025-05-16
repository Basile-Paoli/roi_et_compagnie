from enum import Enum
from typing import Literal


class LocationType(Enum):
    CITY = 0
    MINE = 1
    WORKSHOP = 2
    ORCS_VILLAGE = 3
    FOREST = 4


class Location:

    def __init__(self, value: Literal[2, 3, 4] , location_type: LocationType):
        self.value = value
        self.location_type = location_type


def get_initial_locations():
    return list(
        [
            Location(2, t),
            Location(3, t),
            Location(4, t)
        ]
        for t in LocationType
    )
