from game.gamestate import Game
from interface.menu import show_menu
from interface.game_loop import game_loop
import os


def print_inhabitant_images(initial_inhabitants):
    for inhabitant in initial_inhabitants:
        path = inhabitant.image_path
        exists = os.path.exists(path)
        print(f"{path} - {'OK' if exists else 'MANQUANTE'}")

def main():
    
    nb_joueurs = show_menu()
    state = Game(nb_joueurs)
    print_inhabitant_images(state.inhabitant_deck)
    game_loop(state)

if __name__ == "__main__":
    main()
