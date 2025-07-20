from typing import Optional, Iterable
from game.card_types import KingdomCard, Location, Penalty, get_initial_locations, \
    initial_penalties, LocationType
from game.dice import get_dice, Die
from game.inhabitant import Inhabitant, Elf, Dragon, Sorcerer, Hypnotizer, \
    initial_inhabitants, inhabitant_from_json

import time
import random
import os

random.seed(time.time_ns() ^ os.getpid())


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


def card_from_json(data: dict | int) -> KingdomCard:
    if isinstance(data, int):
        return Penalty(data)
    if data["type"] == "location":
        return Location.from_json(data)
    return inhabitant_from_json(data)


class Player:

    def __init__(self, i: int) -> None:
        self.kingdom: Kingdom = Kingdom()
        self.id = i

    def to_json(self) -> dict:
        return {
            "kingdom": self.kingdom,
            "id": self.id
        }

    @staticmethod
    def from_json(data: dict) -> 'Player':
        player = Player(data["id"])
        player.kingdom = Kingdom([card_from_json(inh) for inh in data["kingdom"]])
        return player


class DieRollState:

    def __init__(self) -> None:
        self.dice = get_dice()
        self.nb_tries = 1

    def to_json(self) -> dict:
        return {
            "dice": [die.to_json() for die in self.dice],
            "nb_tries": self.nb_tries
        }

    @staticmethod
    def from_json(data: dict) -> 'DieRollState':
        state = DieRollState()
        state.dice = [Die.from_json(die) for die in data["dice"]]
        state.nb_tries = data["nb_tries"]
        return state

    def __str__(self) -> str:
        dice_str = ", ".join(str(die) for die in self.dice)
        return f"DieRollState(nb_tries={self.nb_tries}, dice=[{dice_str}])"



class ShopSlot:

    def __init__(self, locations: list[Location], inhabitant: Optional[Inhabitant]=None) -> None:
        self.locations = locations
        self.inhabitant = inhabitant
        self.type = locations[0].location_type

    def to_json(self) -> dict:
        return {
            "locations": self.locations,
            "inhabitant": self.inhabitant,
            "type": self.type
        }

    @staticmethod
    def from_json(data: dict) -> 'ShopSlot':
        locations = [Location.from_json(loc) for loc in data["locations"]]
        inhabitant = inhabitant_from_json(data["inhabitant"]) if data["inhabitant"] else None
        return ShopSlot(locations, inhabitant)


class TargetNeededForDragonException(Exception):
    def __init__(self, dragon: Dragon):
        super().__init__(f"Target needed for Dragon")
        self.dragon = dragon
    pass

class Game:

    def __init__(self, player_count: int) -> None:
        self.inhabitant_deck: list[Inhabitant] = initial_inhabitants()
        self.penalty_deck: list[Penalty] = initial_penalties()
        self.shop = [ShopSlot(locations) for locations in get_initial_locations()]
        self.players = [Player(i) for i in range(player_count)]
        self.current_player_index = 0
        self.die_roll = DieRollState()

        random.shuffle(self.inhabitant_deck)
        random.shuffle(self.penalty_deck)

        self.fill_shop()

    @property
    def player_count(self) -> int:
        return len(self.players)

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    @property
    def inhabitants_displayed(self) -> list[Inhabitant]:
        return [slot.inhabitant for slot in self.shop if slot.inhabitant is not None]

    @property
    def game_over(self) -> bool:
        return any(len(slot.locations) == 0 for slot in self.shop) \
            or len(self.inhabitant_deck) == 0 \
            or len(self.penalty_deck) == 0

    def to_json(self) -> dict:
        return {
            "inhabitant_deck": self.inhabitant_deck,
            "penalty_deck": self.penalty_deck,
            "shop": self.shop,
            "players": self.players,
            "current_player_index": self.current_player_index,
            "die_roll": self.die_roll,
        }

    @staticmethod
    def from_json(data: dict) -> 'Game':
        game = Game(len(data["players"]))
        game.inhabitant_deck = [inhabitant_from_json(inh) for inh in data["inhabitant_deck"]]
        game.penalty_deck = [Penalty(pen) for pen in data["penalty_deck"]]
        game.shop = [ShopSlot.from_json(slot) for slot in data["shop"]]
        game.players = [Player.from_json(player) for player in data["players"]]
        game.current_player_index = data["current_player_index"]
        game.die_roll = DieRollState.from_json(data["die_roll"])
        return game

    def next_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % self.player_count
        self.die_roll = DieRollState()

    def can_reroll(self) -> bool:
        has_elf = isinstance(self.current_player.kingdom[-1], Elf) if self.current_player.kingdom else False
        max_rolls = 4 if has_elf else 3
        return self.die_roll.nb_tries < max_rolls

    def reroll(self, dice: Iterable[Die]) -> None:
        if not self.can_reroll():
            raise ValueError("Cannot reroll, maximum number of tries reached.")
        self.die_roll.nb_tries += 1
        for die in dice:
            die.roll()

    def can_take_inhabitant(self, inhabitant: Inhabitant, player: Player) -> bool:
        if not inhabitant.can_take(die.currentResult for die in self.die_roll.dice):
            return False
        if isinstance(inhabitant, Dragon):
            return player.id != self.current_player.id
        else:
            return player.id == self.current_player.id

    def take_inhabitant(self, inhabitant: Inhabitant, target_player: Player, end_turn = True) -> None:
        slot_with_inhabitant = next((slot for slot in self.shop if slot.inhabitant == inhabitant), None)
        if not slot_with_inhabitant:
            raise ValueError("Inhabitant not found in shop.")

        location_to_take = self.matching_location(inhabitant)
        if location_to_take:
            self.take_location(location_to_take)

        slot_with_inhabitant.inhabitant = None

        target_player.kingdom.append(inhabitant)

        if isinstance(inhabitant, Hypnotizer):
            self.resolve_hypnotizer(slot_with_inhabitant.type)

        self.fill_shop()
        if isinstance(inhabitant, Sorcerer):
            self.die_roll = DieRollState()
        elif end_turn:
            self.next_player()

    def take_penalty(self, target_player: Player) -> None:
        if not self.penalty_deck:
            raise ValueError("No penalties available to take.")
        penalty = self.penalty_deck.pop()
        target_player.kingdom.append(penalty)

    def matching_location(self, inhabitant: Inhabitant) -> Optional[Location]:
        slot = next((loc for loc in self.shop if loc.type == inhabitant.related_location), None)
        if slot and inhabitant == slot.inhabitant:
            return slot.locations[-1]
        return None

    def take_location(self, location: Location) -> None:
        for slot in self.shop:
            if location in slot.locations:
                slot.locations.remove(location)
                self.current_player.kingdom.append(location)
                break

    def resolve_hypnotizer(self, hypnotizer_slot: LocationType) -> None:
        for i, slot in enumerate(self.shop):
            if i == len(self.shop) - 1:
                return
            if slot.type == hypnotizer_slot:
                next_slot = self.shop[i + 1]
                if not next_slot.inhabitant:
                    continue
                if isinstance(next_slot.inhabitant, Dragon) :
                    raise TargetNeededForDragonException(next_slot.inhabitant)
                self.take_inhabitant(next_slot.inhabitant, self.current_player, end_turn=False)

    def fill_shop(self) -> None:
        while any(slot.inhabitant is None for slot in self.shop):
            first_empty = next((i for  i, slot in enumerate(self.shop) if slot.inhabitant is None), -1)
            for i in range(first_empty, -1, -1):
                if i == 0:
                    self.shop[i].inhabitant = self.inhabitant_deck.pop() if self.inhabitant_deck else None
                else:
                    self.shop[i].inhabitant = self.shop[i - 1].inhabitant

