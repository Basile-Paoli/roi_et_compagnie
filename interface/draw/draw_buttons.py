from .utils import draw_button
from game.gamestate import Game

import pygame

def draw_buttons(screen) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
    font = pygame.font.SysFont(None, 30)
    width, height = screen.get_size()
    btn_width, btn_height = 200, 50
    margin = 20

    roll_dice_button_rect = pygame.Rect(
        width - btn_width - margin, height - btn_height * 3 - margin * 3, btn_width, btn_height)
    next_turn_button_rect = pygame.Rect(
        width - btn_width - margin, height - btn_height * 2 - margin * 2, btn_width, btn_height)
    save_button_rect = pygame.Rect(
        width - btn_width - margin, height - btn_height - margin, btn_width, btn_height)

    draw_button(screen, roll_dice_button_rect, "Lancer les dés", font, (70, 130, 180))
    draw_button(screen, next_turn_button_rect, "Changer de tour", font, (180, 70, 80))
    draw_button(screen, save_button_rect, "Sauvegarder", font, (0, 255, 0))
    return roll_dice_button_rect, next_turn_button_rect, save_button_rect
    