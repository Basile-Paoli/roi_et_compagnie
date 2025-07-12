from game.gamestate import Game
from interface.menu import show_menu
from interface.game_screen import game_loop

def main():
    nb_joueurs = show_menu()
    state = Game(nb_joueurs)
    game_loop(state)

if __name__ == "__main__":
    main()