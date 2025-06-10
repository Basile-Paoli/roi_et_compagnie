import unittest
from game.gamestate import Game
import json


class TestJson(unittest.TestCase):

    def test_consistent_json_serialization(self):
        game = Game(3)
        marshaled = json.dumps(game, indent=4, default=lambda o: o.to_json())
        unmarshaled = Game.from_json(json.loads(marshaled))

        remarshaled = json.dumps(unmarshaled, indent=4, default=lambda o: o.to_json())
        
        self.assertEqual(marshaled, remarshaled)
