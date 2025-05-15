import unittest

from game.dice import Die, DiceColor
from game.inhabitant import Gnome
from game.location import LocationType

class TestInhabitant(unittest.TestCase):
    def test_gnome_can_take(self) -> None:
        g = Gnome(LocationType.CITY, DiceColor.RED, 2)
        dice: list[Die] = [(1, DiceColor.RED), (2, DiceColor.BLUE)]
        self.assertFalse(g.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.RED)]
        self.assertTrue(g.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.RED), (3, DiceColor.BLUE)]
        self.assertTrue(g.can_take(dice))

    
if __name__ == "__main__":
    unittest.main()