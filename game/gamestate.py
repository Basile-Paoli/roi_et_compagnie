from typing import Optional
from game.inhabitant import Inhabitant
from game.location import Location, get_initial_locations

type Penalty = int

class Player:
    def __init__(self) -> None:
        self.kingdom: list[Inhabitant | Location | Penalty] = []

class Game:
    def __init__(self) -> None:
        self.inhabitant_deck: list[Inhabitant] = []
        self.penalty_deck: list[Penalty] = []
        self.locations = get_initial_locations()
        self.displayed_inhabitants: list[Optional[Inhabitant]] = [None, None, None, None, None]
        self.players: list[Player] = []
