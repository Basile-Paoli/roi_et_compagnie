from typing import  Optional 
from game.card_types import KingdomCard, Location, Penalty, get_initial_locations
from game.inhabitant import Inhabitant


class Kingdom(list[KingdomCard]):

    def total_value(self) -> int:
        return sum(inh.value(self) for inh in self)

    @property
    def inhabitants(self):
        return (inh for inh in self if isinstance(inh, Inhabitant))

    @property
    def locations(self):
        return (loc for loc in self if isinstance(loc, Location))
    
    @property
    def penalties(self):
        return (pen for pen in self if isinstance(pen, Penalty))


class Player:

    def __init__(self) -> None:
        self.kingdom: Kingdom = Kingdom()


class DieRollState:
    pass


class Game:

    def __init__(self, player_count: int) -> None:
        self.inhabitant_deck: list[Inhabitant] = []
        self.penalty_deck: list[Penalty] = []
        self.locations = get_initial_locations()
        self.displayed_inhabitants: list[Optional[Inhabitant]] = [None, None, None, None, None]
        self.players = [Player() for _ in range(player_count)]
        self.current_player_index = 0
        self.die_roll = DieRollState()
    
    @property
    def player_count(self) -> int:
        return len(self.players)

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]
