import pygame
from typing import Tuple

from game.gamestate import Game, Dragon, Player

from .draw.draw_locations import draw_locations
from .draw.draw_inhabitants import draw_inhabitants
from .draw.draw_player_deck import draw_player_deck
from .draw.draw_penalty_deck import draw_penalty_deck
from .draw.draw_buttons import draw_buttons
from .draw.draw_dice_status import draw_dice_status
from .draw.draw_dragon_selection import draw_dragon_selection_overlay


from .game_result import game_result

width_init = 1920
height_init = 1080

def game_loop(state: Game):
    pygame.init()
    screen = pygame.display.set_mode((width_init, height_init), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    selected_dice_indices: list[int] = []
    dragon_selection = None
    dragon_selection_rects: list[Tuple[pygame.Rect, Player]] = []

    running = True

    while running:

        screen.fill((0, 100, 0))

        draw_locations(state, screen)
        inhabitant_rects = draw_inhabitants(state, screen)
        draw_player_deck(state.current_player, screen)
        draw_penalty_deck(state, screen)
        die_rects = draw_dice_status(state, screen, selected_dice_indices)

        roll_dice_button_rect, next_turn_button_rect, save_button_rect = draw_buttons(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif dragon_selection and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for rect, p in dragon_selection_rects:
                    if rect.collidepoint(pos):
                        state.take_inhabitant(dragon_selection[0], p)
                        dragon_selection = None
                        break
                continue

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()


                if roll_dice_button_rect.collidepoint(mouse_pos):
                    if state.can_reroll():
                        if selected_dice_indices:
                            dice_to_reroll = [state.die_roll.dice[i] for i in selected_dice_indices]
                        else:
                            dice_to_reroll = state.die_roll.dice

                        state.reroll(dice_to_reroll)
                        selected_dice_indices.clear()



                elif next_turn_button_rect.collidepoint(mouse_pos):
                    try:
                        state.take_penalty(state.current_player)
                        state.next_player()
                    except:
                        print("next turn error")

                elif save_button_rect.collidepoint(mouse_pos):
                    # TODO : Save the game
                    print("Should save the game, but rn no")

                else:
                    for idx, rect in enumerate(die_rects):
                        if rect.collidepoint(mouse_pos):
                            if idx in selected_dice_indices:
                                selected_dice_indices.remove(idx)
                            else:
                                selected_dice_indices.append(idx)
                            break

                    for rect, inhabitant, slot_index in inhabitant_rects:
                        if rect.collidepoint(mouse_pos):
                            print(f"Habitant {inhabitant} cliqué dans le slot {slot_index}")
                            if state.can_take_inhabitant(inhabitant, state.current_player) :
                                state.take_inhabitant(inhabitant, state.current_player)
                            elif isinstance(inhabitant, Dragon):
                                other_players = [p for p in state.players if p.id != state.current_player.id]
                                if len(other_players) == 1:
                                    target = other_players[0]
                                    state.take_inhabitant(inhabitant, target)
                                else:
                                    dragon_selection = (inhabitant, other_players)
                                break
                            break
        

        if dragon_selection:
            inhabitant, possible_targets = dragon_selection
            dragon_selection_rects = draw_dragon_selection_overlay(screen, possible_targets)
        else:
            dragon_selection_rects = []
        
        
        if state.game_over:
            game_result(state)
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
