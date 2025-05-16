import unittest

from game.dice import  DiceColor,  DieResult
from game.gamestate import Kingdom
from game.inhabitant import Bourgeois, Elf, Fairy, Gnome, Dwarf, Orc, MushKobold, Sorcerer
from game.location import LocationType


class TestInhabitant(unittest.TestCase):

    def test_gnome_can_take(self) -> None:
        g = Gnome(LocationType.CITY, 8, DiceColor.RED, 2)
        dice: list[DieResult] = [(1, DiceColor.RED), (2, DiceColor.BLUE)]
        self.assertFalse(g.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.RED)]
        self.assertTrue(g.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.RED), (3, DiceColor.BLUE)]
        self.assertTrue(g.can_take(dice))

    def test_bourgeois_can_take(self) -> None:
        b = Bourgeois(LocationType.CITY, 5, 'even')

        dice: list[DieResult] = [(1, DiceColor.RED), (2, DiceColor.BLUE)]
        self.assertFalse(b.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.BLUE), (3, DiceColor.RED)]
        self.assertFalse(b.can_take(dice))
        dice = [(2, DiceColor.RED), (4, DiceColor.BLUE), (2, DiceColor.GREEN)]
        self.assertTrue(b.can_take(dice))

    def test_elf_can_take(self) -> None:
        e = Elf(LocationType.CITY, 5, 4)
        dice: list[DieResult] = [(1, DiceColor.RED), (2, DiceColor.BLUE), (3, DiceColor.GREEN)]
        self.assertFalse(e.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.BLUE), (3, DiceColor.GREEN), (3, DiceColor.RED), (4, DiceColor.GREEN)]
        self.assertTrue(e.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.BLUE), (3, DiceColor.GREEN), (3, DiceColor.RED), (5, DiceColor.GREEN)]
        self.assertFalse(e.can_take(dice))

    def test_dwarf_can_take(self) -> None:
        d = Dwarf(LocationType.CITY, 5, 4, 3)
        dice: list[DieResult] = [(1, DiceColor.RED), (2, DiceColor.BLUE), (3, DiceColor.GREEN)]
        self.assertFalse(d.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.BLUE), (3, DiceColor.GREEN), (4, DiceColor.RED), (4, DiceColor.GREEN)]
        self.assertFalse(d.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.BLUE), (3, DiceColor.GREEN), (4, DiceColor.RED), (4, DiceColor.GREEN), (4, DiceColor.BLUE)]
        self.assertTrue(d.can_take(dice))
        dice = [(4, DiceColor.RED), (2, DiceColor.BLUE), (3, DiceColor.GREEN), (4, DiceColor.RED), (4, DiceColor.GREEN), (4, DiceColor.BLUE)]
        self.assertTrue(d.can_take(dice))
        
    def test_orc_can_take(self) -> None:
        o = Orc(LocationType.CITY, 5, [1, 2, 3])
        dice: list[DieResult] = [(1, DiceColor.RED), (2, DiceColor.BLUE), (2, DiceColor.GREEN), (3, DiceColor.RED), (3, DiceColor.GREEN), (4, DiceColor.RED)]
        self.assertFalse(o.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.BLUE), (2, DiceColor.GREEN), (3, DiceColor.RED), (3, DiceColor.GREEN), (3, DiceColor.RED)]
        self.assertTrue(o.can_take(dice))

    def test_mush_kobold_can_take(self) -> None:
        m = MushKobold(LocationType.CITY, 5, 4)
        dice: list[DieResult] = [(1, DiceColor.RED), (2, DiceColor.RED), (3, DiceColor.RED), (4, DiceColor.GREEN), (5, DiceColor.GREEN), (6, DiceColor.BLUE)]
        self.assertFalse(m.can_take(dice))
        dice = [(1, DiceColor.RED), (2, DiceColor.RED), (3, DiceColor.RED), (4, DiceColor.RED), (5, DiceColor.GREEN), (6, DiceColor.GREEN)]
        self.assertTrue(m.can_take(dice))

    def test_sorcerer_can_take(self) -> None:
        s = Sorcerer(LocationType.CITY, 5, {
            DiceColor.RED: 2,
            DiceColor.GREEN: 1,
            DiceColor.BLUE: 2
        })

        dice: list[DieResult] = [(1, DiceColor.RED), (2, DiceColor.RED), (3, DiceColor.RED), (4, DiceColor.GREEN), (5, DiceColor.GREEN), (6, DiceColor.BLUE)]
        self.assertFalse(s.can_take(dice))
        dice = [(1, DiceColor.RED), (3, DiceColor.RED), (4, DiceColor.GREEN), (5, DiceColor.GREEN), (6, DiceColor.BLUE), (6, DiceColor.BLUE)]
        self.assertTrue(s.can_take(dice))

    def test_fairy_can_take(self) -> None:
        f = Fairy(LocationType.CITY, {
            DiceColor.RED: 2,
            DiceColor.GREEN: 1,
            DiceColor.BLUE: 2
        })

        dice: list[DieResult] = [(1, DiceColor.RED), (2, DiceColor.RED), (3, DiceColor.RED), (4, DiceColor.GREEN), (5, DiceColor.GREEN), (6, DiceColor.BLUE)]
        self.assertFalse(f.can_take(dice))
        dice = [(1, DiceColor.RED), (3, DiceColor.RED), (4, DiceColor.GREEN), (5, DiceColor.GREEN), (6, DiceColor.BLUE), (6, DiceColor.BLUE)]
        self.assertTrue(f.can_take(dice))

    def test_fairy_value(self) -> None:
        f = Fairy(LocationType.CITY, {
            DiceColor.RED: 2,
            DiceColor.GREEN: 1,
            DiceColor.BLUE: 2
        })
        kingdom: Kingdom = Kingdom([
            Elf(LocationType.CITY, 5, 4),
            Dwarf(LocationType.CITY, 5, 4, 3),
            Orc(LocationType.CITY, 5, [1, 2, 3]),
            MushKobold(LocationType.CITY, 5, 4),
            Sorcerer(LocationType.CITY, 5, {
                DiceColor.RED: 2,
                DiceColor.GREEN: 1,
                DiceColor.BLUE: 2
            })
        ])

        self.assertEqual(f.value(kingdom), 1)

        kingdom = Kingdom([
            Dwarf(LocationType.CITY, 5, 4, 3),
            Orc(LocationType.CITY, 5, [1, 2, 3]),
            MushKobold(LocationType.CITY, 5, 4),
            Fairy(LocationType.CITY, {
                DiceColor.RED: 2,
                DiceColor.GREEN: 1,
                DiceColor.BLUE: 2
            }),
        ])

        self.assertEqual(f.value(kingdom), 2)

        kingdom = Kingdom([
            Fairy(LocationType.CITY, {
                DiceColor.RED: 2,
                DiceColor.GREEN: 1,
                DiceColor.BLUE: 2
            }),
            Fairy(LocationType.MINE, {
                DiceColor.RED: 1,
                DiceColor.GREEN: 3,
            }),
            Fairy(LocationType.FOREST, {
                DiceColor.RED: 2,
                DiceColor.GREEN: 1,
                DiceColor.BLUE: 2
            }),
        ])

        self.assertEqual(f.value(kingdom), 3)


if __name__ == "__main__":
    unittest.main()
