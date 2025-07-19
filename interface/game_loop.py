import pygame
from game.gamestate import Game
from .draw_locations import draw_locations
from .draw_inhabitants import draw_inhabitants
from .draw_player_deck import draw_player_deck
from .draw_penalty_deck import draw_penalty_deck
from .draw_buttons import draw_buttons
from .draw_dice_status import draw_dice_status

width_init = 1920
height_init = 1080

def game_loop(state: Game):
    pygame.init()
    screen = pygame.display.set_mode((width_init, height_init), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    running = True

    while running:
        screen.fill((0, 100, 0))

        draw_locations(state, screen)
        inhabitant_rects = draw_inhabitants(state, screen)
        draw_player_deck(state.current_player, screen)
        draw_penalty_deck(state, screen)
        draw_dice_status(state, screen)

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
                    
                else:
                    for rect, inhabitant, slot_index in inhabitant_rects:
                        if rect.collidepoint(mouse_pos):
                            print(f"Habitant {inhabitant} cliqué dans le slot {slot_index}")
                            if state.can_take_inhabitant(inhabitant, state.current_player) :
                                state.take_inhabitant(inhabitant, state.current_player)
                            break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
