import pygame
import collections

from game.card_types import Location, Penalty
from game.inhabitant import Inhabitant
from game.gamestate import Player
from .image_cache import get_card_image


def draw_player_deck(player, screen):
    width, height = screen.get_size()

    card_left_ratio = 0.20
    panel_left = int(width * 0.02)
    panel_width = int(width * card_left_ratio)
    card_width = int(panel_width * 0.8)
    card_height = int(card_width * 1.4)

    x = panel_left
    y = height - card_height - 32

    if player.kingdom:
        card = player.kingdom[-1]
        if hasattr(card, "image_path"):
            image = get_card_image(image, (card_width, card_height))
            screen.blit(image, (x, y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, card_width, card_height), 3)
    else:
        pygame.draw.rect(screen, (200, 200, 200), (x, y, card_width, card_height), 3)

    font = pygame.font.SysFont(None, 24)
    line_height = font.get_linesize()

    card_counter = collections.Counter()

    for card in player.kingdom:
        if isinstance(card, Inhabitant):
            card_type = type(card).__name__
        elif isinstance(card, Location):
            card_type = type(card).__name__
        elif isinstance(card, Penalty):
            card_type = "Malus"
        else:
            card_type = "Carte inconnue"
        card_counter[card_type] += 1

    card_lines = [f"{count} {name}{'s' if count>1 and not name.endswith('s') else ''}" for name, count in sorted(card_counter.items())]

    text_x = x + card_width + 18
    text_y = y

    for i, line in enumerate(card_lines):
        text_surf = font.render(line, True, (255, 255, 255))
        screen.blit(text_surf, (text_x, text_y + i * line_height))
    
    total_points = player.kingdom.total_value() if hasattr(player.kingdom, "total_value") else 0
    points_line = f"Points : {total_points}"
    text_surf = font.render(points_line, True, (255, 215, 0))
    screen.blit(text_surf, (text_x, text_y + len(card_lines) * line_height + 8))