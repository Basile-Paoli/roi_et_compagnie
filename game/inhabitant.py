from abc import ABC, abstractmethod
from collections import Counter
from typing import Iterable, Literal 

from game.dice import DiceColor, DiceValue,  DieResult
from game.location import  LocationType


class Inhabitant(ABC):

    def __init__(self, color: LocationType) -> None:
        self.color = color

    @abstractmethod
    def value(self, kingdom: Iterable[object]) -> int:
        pass

    @abstractmethod
    def can_take(self, dice: Iterable[DieResult]) -> bool:
        pass


class Gnome(Inhabitant):

    def __init__(self, color: LocationType, value: int, dice_color: DiceColor, dice_count: int) -> None:
        super().__init__(color)
        self.dice_color = dice_color
        self.dice_count = dice_count
        self._value = value

    def value(self, kingdom: Iterable[object]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return sum(1 for die in dice if die[1] == self.dice_color) >= self.dice_count


class Bourgeois(Inhabitant):

    def __init__(self, color: LocationType, value: int, parity: Literal['odd', 'even']) -> None:
        super().__init__(color)
        self._value = value
        self.parity = parity

    def value(self, kingdom: Iterable[object]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return all(d[0] % 2 == (1 if self.parity == 'odd' else 0) for d in dice)

        
class Elf(Inhabitant):

    def __init__(self, color: LocationType, value: int, sequence_length: int) -> None:
        super().__init__(color)
        self.sequence_length = sequence_length
        self._value = value

    def value(self, kingdom: Iterable[object]) -> int:
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
        

class Dwarf(Inhabitant):

    def __init__(self, color: LocationType, value: int, dice_value: DiceValue, dice_count: int) -> None:
        super().__init__(color)
        self._value = value
        self.dice_value = dice_value
        self.dice_count = dice_count

    def value(self, kingdom: Iterable[object]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        return sum(1 for die in dice if die[0] == self.dice_value) >= self.dice_count

        
class Orc(Inhabitant):

    def __init__(self, color: LocationType, value: int, dice_sets: list[int]) -> None:
        super().__init__(color)
        self._value = value
        self.dice_sets = dice_sets

    def value(self, kingdom: Iterable[object]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        dice_count = Counter(d[0] for d in dice)
        sorted_dice_values = sorted(dice_count.values(), reverse=True)
        sorted_sets = sorted(self.dice_sets, reverse=True)
        return all(sorted_dice_values[i] >= s for i, s in enumerate(sorted_sets))


class MushKobold(Inhabitant):

    def __init__(self, color: LocationType, value: int, dice_count: int) -> None:
        super().__init__(color)
        self._value = value
        self.dice_count = dice_count

    def value(self, kingdom: Iterable[object]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        dice_by_color = Counter(d[1] for d in dice)
    
        return any(count >= self.dice_count for count in dice_by_color.values())


class Sorcerer(Inhabitant):

    def __init__(self, color: LocationType, value: int, dice_colors: dict[DiceColor, int]) -> None:
        super().__init__(color)
        self._value = value
        self.dice_colors = dice_colors

    def value(self, kingdom: Iterable[object]) -> int:
        return self._value

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        dice_by_color = Counter(d[1] for d in dice)
        return all(dice_by_color.get(color, 0) >= count for color, count in self.dice_colors.items())


class Fairy(Inhabitant):

    def __init__(self, color: LocationType, dice_colors: dict[DiceColor, int]) -> None:
        super().__init__(color)
        self.dice_colors = dice_colors

    def value(self, kingdom: Iterable[object]) -> int:
        return sum(1 for card in kingdom if isinstance(card, Fairy))

    def can_take(self, dice: Iterable[DieResult]) -> bool:
        dice_by_color = Counter(d[1] for d in dice)
        return all(dice_by_color.get(color, 0) >= count for color, count in self.dice_colors.items())

