from game.inhabitant import Inhabitant
from game.gamestate import Game
from .image_cache import get_card_image
import pygame

def draw_inhabitants(state: Game, screen) -> list[tuple[pygame.Rect, Inhabitant, int]]:
    font = pygame.font.SysFont(None, 20)
    width, height = screen.get_size()
    count = len(state.inhabitants_displayed)
    if count == 0:
        return []

    card_left_ratio = 0.80
    usable_width = width * card_left_ratio
    spacing_ratio = 0.04
    total_spacing = (count + 1) * spacing_ratio * usable_width
    card_width = int((usable_width - total_spacing) / count)
    card_height = int(card_width / 1.5)
    x_offset = int(width * 0.02)
    y_offset = int(height * 0.3)
    inhabitant_width = int(card_width * 0.70)
    inhabitant_height = int(inhabitant_width * 1.4)
    spacing_x = card_width + int(spacing_ratio * usable_width)

    inhabitant_rects = []
    for i, inhabitant in enumerate(state.inhabitants_displayed):
        inhabitant_x = x_offset + i * spacing_x + (card_width - inhabitant_width) // 2
        inhabitant_y = y_offset
        rect = pygame.Rect(inhabitant_x, inhabitant_y, inhabitant_width, inhabitant_height)
        if hasattr(inhabitant, "image_path"):
            try:
                img = get_card_image(inhabitant.image_path, (inhabitant_width, inhabitant_height))
                screen.blit(img, (inhabitant_x, inhabitant_y))
            except FileNotFoundError:
                pygame.draw.rect(screen, (70, 70, 140), rect)
                err = font.render("Image ?", True, (255, 0, 0))
                screen.blit(err, (inhabitant_x + 5, inhabitant_y + inhabitant_height // 2 - 10))
        else:
            pygame.draw.rect(screen, (70, 70, 140), rect)
            label = font.render(f"{type(inhabitant).__name__}", True, (255, 255, 255))
            screen.blit(label, (inhabitant_x + 5, inhabitant_y + inhabitant_height // 2 - 10))
        inhabitant_rects.append((rect, inhabitant, i))

    return inhabitant_rects
