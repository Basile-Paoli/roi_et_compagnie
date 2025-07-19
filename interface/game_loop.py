import pygame
from game.gamestate import Game
from .draw_locations import draw_locations
from .draw_inhabitants import draw_inhabitants
from .draw_player_deck import draw_player_deck
from .draw_penalty_deck import draw_penalty_deck

from .utils import draw_button

def game_loop(state: Game):
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    roll_dice_button_rect = pygame.Rect(555, 500, 180, 40)
    next_turn_button_rect = pygame.Rect(555, 550, 180, 40)

    running = True

    while running:
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


        screen.fill((0, 100, 0))
        draw_locations(state, screen)
        draw_inhabitants(state, screen)
        draw_player_deck(state.current_player, screen)
        draw_penalty_deck(state, screen)
        draw_button(screen, roll_dice_button_rect, "Lancer les dés", font, (70, 130, 180))
        draw_button(screen, next_turn_button_rect, "Changer de tour", font, (180, 70, 80))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
