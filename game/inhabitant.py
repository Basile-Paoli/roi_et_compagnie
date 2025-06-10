from collections import Counter
from typing import Iterable, Literal, Optional

from game.card_types import Inhabitant, KingdomCard, LocationType
from game.dice import DiceColor, DiceValue, DieResult


class Bourgeois(Inhabitant):

    def __init__(self, value: int, parity: Literal['odd', 'even']) -> None:
        self._value = value
        self.parity = parity

    @property
    def related_location(self) -> Optional[LocationType]:
        return LocationType.CITY

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return all(d[0] % 2 == (1 if self.parity == 'odd' else 0) for d in dice)
        
    def to_json(self) -> dict:
        return {
            'type': 'bourgeois',
            "value": self._value,
            "parity": self.parity
        }


class Elf(Inhabitant):

    def __init__(self, value: int, sequence_length: int) -> None:
        self.sequence_length = sequence_length
        self._value = value

    @property
    def related_location(self) -> LocationType:
        return LocationType.CITY

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value

    @staticmethod
    def longest_sequence(dice: Iterable[DieResult]) -> int:
        sorted_dice_values = sorted(set(d[0] for d in dice))
        max_sequence = 0
        current_sequence = 0
        for i, val in enumerate(sorted_dice_values):
            if i == 0 or val == sorted_dice_values[i - 1] + 1:
                current_sequence += 1
            else:
                max_sequence = max(max_sequence, current_sequence)
                current_sequence = 1
        return max(max_sequence, current_sequence)

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return Elf.longest_sequence(dice) >= self.sequence_length
        
    def to_json(self) -> dict:
        return {
            "type": "elf",
            "value": self._value,
            "sequence_length": self.sequence_length
        }


class Dwarf(Inhabitant):

    def __init__(self, value: int, dice_value: DiceValue, dice_count: int) -> None:
        self._value = value
        self.dice_value = dice_value
        self.dice_count = dice_count

    @property
    def related_location(self) -> LocationType:
        return LocationType.MINE

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return sum(1 for die in dice if die[0] == self.dice_value) >= self.dice_count
        
    def to_json(self) -> dict:
        return {
            "type": "dwarf",
            "value": self._value,
            "dice_value": self.dice_value,
            "dice_count": self.dice_count
        }


class Gnome(Inhabitant):

    def __init__(self, value: int, dice_color: DiceColor, dice_count: int) -> None:
        self.dice_color = dice_color
        self.dice_count = dice_count
        self._value = value

    @property
    def related_location(self) -> LocationType:
        return LocationType.WORKSHOP

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return sum(1 for die in dice if die[1] == self.dice_color) >= self.dice_count
        
    def to_json(self) -> dict:
        return {
            "type": "gnome",
            "value": self._value,
            "dice_color": self.dice_color,
            "dice_count": self.dice_count
        }


class Orc(Inhabitant):

    def __init__(self, value: int, dice_sets: list[int]) -> None:
        self._value = value
        self.dice_sets = dice_sets

    @property
    def related_location(self) -> LocationType:
        return LocationType.ORCS_VILLAGE

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        dice_count = Counter(d[0] for d in dice)
        sorted_dice_values = sorted(dice_count.values(), reverse=True)
        sorted_sets = sorted(self.dice_sets, reverse=True)
        return all(sorted_dice_values[i] >= s for i, s in enumerate(sorted_sets))
        
    def to_json(self) -> dict:
        return {
            "type": "orc",
            "value": self._value,
            "dice_sets": self.dice_sets
        }


class MushKobold(Inhabitant):

    def __init__(self, value: int, dice_count: int) -> None:
        self._value = value
        self.dice_count = dice_count

    @property
    def related_location(self) -> LocationType:
        return LocationType.FOREST

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        dice_by_color = Counter(d[1] for d in dice)

        return any(count >= self.dice_count for count in dice_by_color.values())
        
    def to_json(self) -> dict:
        return {
            "type": "mush_kobold",
            "value": self._value,
            "dice_count": self.dice_count
        }


class Sorcerer(Inhabitant):

    def __init__(self, value: int, dice_colors: dict[DiceColor, int]) -> None:
        self._value = value
        self.dice_colors = dice_colors

    @property
    def related_location(self) -> LocationType:
        return LocationType.FOREST

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        dice_by_color = Counter(d[1] for d in dice)
        return all(dice_by_color.get(color, 0) >= count for color, count in self.dice_colors.items())
        
    def to_json(self) -> dict:
        return {
            "type": "sorcerer",
            "value": self._value,
            "dice_colors": {color.to_json(): count for color, count in self.dice_colors.items()}
        }


class Fairy(Inhabitant):

    def __init__(self, dice_colors: dict[DiceColor, int]) -> None:
        self.dice_colors = dice_colors

    @property
    def related_location(self) -> LocationType:
        return LocationType.FOREST

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return sum(1 for card in kingdom if isinstance(card, Fairy))

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        dice_by_color = Counter(d[1] for d in dice)
        return all(dice_by_color.get(color, 0) >= count for color, count in self.dice_colors.items())
        
    def to_json(self) -> dict:
        return {
            "type": "fairy",
            "dice_colors": {color.to_json(): count for color, count in self.dice_colors.items()}
        }


class Hypnotizer(Inhabitant):

    def __init__(self, value: int, max_dice_val: int) -> None:
        self._value = value
        self.max_dice_val = max_dice_val

    @property
    def related_location(self) -> Optional[LocationType]:
        return None

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return sum(d[0] for d in dice) <= self.max_dice_val
        
    def to_json(self) -> dict:
        return {
            "type": "hypnotizer",
            "value": self._value,
            "max_dice_val": self.max_dice_val
        }


class Dragon(Inhabitant):

    def __init__(self, value: int, min_dice_val: int) -> None:
        self._value = value
        self.min_dice_val = min_dice_val

    @property
    def related_location(self):
        return None

    def value(self, kingdom: Iterable[KingdomCard]) -> int:
        return -self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return sum(d[0] for d in dice) >= self.min_dice_val
        
    def to_json(self) -> dict:
        return {
            "type": "dragon",
            "value": self._value,
            "min_dice_val": self.min_dice_val
        }


def initial_inhabitants() -> list[Inhabitant]:
    return [
        Bourgeois(5, 'even'),
        Bourgeois(5, 'odd'),
        
        Elf(7, 6),
        Elf(3, 5),
        Elf(1, 4),
        
        Dwarf(10, 6, 5),
        Dwarf(10, 1, 5),
        Dwarf(6, 6, 4),
        Dwarf(6, 4, 4),
        Dwarf(6, 3, 4),
        Dwarf(4, 4, 3),
        Dwarf(4, 3, 3),
        Dwarf(4, 1, 3),
        
        Gnome(8, DiceColor.BLUE, 6),
        Gnome(3, DiceColor.BLUE, 5),
        Gnome(3, DiceColor.RED, 5),
        Gnome(2, DiceColor.RED, 4),
        Gnome(2, DiceColor.GREEN, 4),
        Gnome(1, DiceColor.GREEN, 3),
        
        Orc(7, [5]),
        Orc(3, [4]),
        Orc(2, [3]),
        Orc(8, [4, 2]),
        Orc(7, [2, 2, 2]),
        Orc(3, [3, 2]),
        Orc(1, [2, 2]),
        
        MushKobold(7, 6),
        MushKobold(2, 5),
        MushKobold(1, 4),
        
        Sorcerer(3, {DiceColor.BLUE: 3, DiceColor.RED: 3}),
        Sorcerer(2, {DiceColor.BLUE: 2, DiceColor.RED: 2, DiceColor.GREEN: 2}),
        
        Fairy({DiceColor.RED: 3, DiceColor.BLUE: 2}),
        Fairy({DiceColor.RED: 2, DiceColor.GREEN: 3}),
        Fairy({DiceColor.BLUE: 3, DiceColor.GREEN: 2}),
        Fairy({DiceColor.BLUE: 2, DiceColor.GREEN: 2}),
        Fairy({DiceColor.RED: 2, DiceColor.GREEN: 2}),
        
        Hypnotizer(1, 12),
        
        Dragon(6, 30),
        Dragon(4, 28),
        Dragon(2, 25),
    ]
