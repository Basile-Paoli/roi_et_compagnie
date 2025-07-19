import pygame
from game.gamestate import Game
from .draw_locations import draw_locations
from .draw_inhabitants import draw_inhabitants
from .draw_player_deck import draw_player_deck
from .draw_penalty_deck import draw_penalty_deck
from .draw_buttons import draw_buttons

width_init = 1920
height_init = 1080

def game_loop(state: Game):
    pygame.init()
    screen = pygame.display.set_mode((width_init, height_init), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    running = True

    while running:
        screen.fill((0, 100, 0))

        # Rendu du jeu...
        draw_locations(state, screen)
        draw_inhabitants(state, screen)
        draw_player_deck(state.current_player, screen)
        draw_penalty_deck(state, screen)

        # Dessin ET récupération des boutons à chaque frame
        roll_dice_button_rect, next_turn_button_rect = draw_buttons(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if roll_dice_button_rect.collidepoint(mouse_pos):
                    print("🎲 Lancer les dés")
                    if state.can_reroll():
                        state.reroll(state.die_roll.dice)
                    else:
                        print("❌ Nombre maximum de relances atteint")
                elif next_turn_button_rect.collidepoint(mouse_pos):
                    print("⏭️ Tour suivant")
                    state.next_player()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
