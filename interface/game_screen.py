import pygame
from game.gamestate import Game

def game_loop(state: Game):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Appelle la logique du jeu
        state.update()

        # Affiche l'état du jeu
        screen.fill((0, 100, 0))
        state.draw(screen)  # À implémenter dans GameState ou via une fonction dédiée

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
