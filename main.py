from game.gamestate import Game
from interface.menu import menu
from interface.game_loop import game_loop
import os

from interface.gamestate_manager import load_gamestate


def print_inhabitant_images(initial_inhabitants):
    for inhabitant in initial_inhabitants:
        path = inhabitant.image_path
        exists = os.path.exists(path)
        print(f"{path} - {'OK' if exists else 'MANQUANTE'}")

def main():
    while True :
        choice = menu()
        if choice == -1:
            state = Game(1).from_json(load_gamestate())
        elif choice in (2, 3, 4):
            state = Game(choice)
        else :
            break

        print_inhabitant_images(state.inhabitant_deck)
        game_loop(state)

if __name__ == "__main__":
    main()
