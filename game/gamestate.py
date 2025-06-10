from typing import Optional, Iterable
from game.card_types import KingdomCard, Location, Penalty, get_initial_locations
from game.dice import get_dice, Die
from game.inhabitant import Inhabitant, Elf, Dragon, Sorcerer, Hypnotizer


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

    def __init__(self, i: int) -> None:
        self.kingdom: Kingdom = Kingdom()
        self.id = i


class DieRollState:

    def __init__(self) -> None:
        self.dice = get_dice()
        self.nb_tries = 1


class ShopSlot:

    def __init__(self, locations: list[Location], inhabitant: Optional[Inhabitant]=None) -> None:
        self.locations = locations
        self.inhabitant = inhabitant
        self.type = locations[0].location_type


class Game:

    def __init__(self, player_count: int) -> None:
        self.inhabitant_deck: list[Inhabitant] = []
        self.penalty_deck: list[Penalty] = []
        self.shop = [ShopSlot(locations) for locations in get_initial_locations()]
        self.players = [Player(i) for i in range(player_count)]
        self.current_player_index = 0
        self.die_roll = DieRollState()

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
        if not inhabitant.can_take(self.die_roll.dice):
            return False
        if isinstance(inhabitant, Dragon):
            return player.id != self.current_player.id
        else:
            return player.id == self.current_player.id

    def take_inhabitant(self, inhabitant: Inhabitant, target_player: Player) -> None:
        location_to_take = self.matching_location(inhabitant)
        if location_to_take:
            self.take_location(location_to_take)

        target_player.kingdom.append(inhabitant)

        if isinstance(inhabitant, Hypnotizer):
            self.resolve_hypnotizer()

        self.fill_shop()
        if isinstance(inhabitant, Sorcerer):
            self.die_roll = DieRollState()
        else:
            self.next_player()

    def matching_location(self, inhabitant) -> Optional[Location]:
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

    def resolve_hypnotizer(self) -> None:
        for i, slot in enumerate(self.shop):
            if i == len(self.shop) - 1:
                return
            if isinstance(slot.inhabitant, Hypnotizer):
                next_slot = self.shop[i + 1]
                if not next_slot.inhabitant:
                    continue
                self.take_inhabitant(next_slot.inhabitant, self.current_player)

    def fill_shop(self) -> None:
        while any(slot.inhabitant is None for slot in self.shop):
            first_empty = next((i for  i, slot in enumerate(self.shop) if slot.inhabitant is None), -1)
            for i in range(first_empty, -1, -1):
                if i == 0:
                    self.shop[i].inhabitant = self.inhabitant_deck.pop() if self.inhabitant_deck else None
                else:
                    self.shop[i].inhabitant = self.shop[i - 1].inhabitant

