import pygame
from game.card_types import Penalty
from game.gamestate import Game
from .image_cache import get_card_image
import pygame
from game.card_types import Penalty


def draw_penalty_deck(state: Game, screen, card_left_ratio=0.90):
    """Dessine la carte de pénalité dans les 10% droits de l’écran, alignée en haut avec les locations."""
    width, height = screen.get_size()

    shop_count = max(len(state.shop), 1)
    spacing_ratio = 0.04
    usable_width = width * card_left_ratio
    total_spacing = (shop_count + 1) * spacing_ratio * usable_width
    card_width_landscape = int((usable_width - total_spacing) / shop_count)
    card_height_landscape = int(card_width_landscape / 1.5)
    y_offset = int(height * 0.03)

    penalty_panel_left = int(width * card_left_ratio)
    penalty_panel_width = int(width * (1 - card_left_ratio))

    penalty_width = int(penalty_panel_width * 0.8)
    penalty_height = int(penalty_width * 1.5)

    penalty_x = penalty_panel_left + (penalty_panel_width - penalty_width) // 2
    penalty_y = y_offset

    if len(state.penalty_deck) > 0:
        penalty = state.penalty_deck[-1]
        if hasattr(penalty, "image_path"):
            try:
                image = get_card_image(penalty.image_path, (penalty_width, penalty_height))
                screen.blit(image, (penalty_x, penalty_y))
            except FileNotFoundError:
                pygame.draw.rect(screen, (180, 0, 0), (penalty_x, penalty_y, penalty_width, penalty_height))
        else:
            pygame.draw.rect(screen, (180, 0, 0), (penalty_x, penalty_y, penalty_width, penalty_height))
    else:
        font_small = pygame.font.SysFont(None, 20)
        aucun_label = font_small.render("Pioche vide", True, (255, 255, 255))
        screen.blit(aucun_label, (penalty_x, penalty_y + 10))

