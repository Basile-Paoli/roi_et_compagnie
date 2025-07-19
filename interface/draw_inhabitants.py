from game.inhabitant import Inhabitant
from game.gamestate import Game
import pygame

def draw_inhabitants(state: Game, screen):
    font = pygame.font.SysFont(None, 20)

    width, height = screen.get_size()
    card_left_ratio = 0.80
    usable_width = width * card_left_ratio
    shop_count = max(len(state.shop), 1)
    spacing_ratio = 0.04
    total_spacing = (shop_count + 1) * spacing_ratio * usable_width
    card_width = int((usable_width - total_spacing) / shop_count)
    card_height = int(card_width / 1.5)
    x_offset = int(width * 0.02)
    y_offset = int(height * 0.03)
    spacing_x = card_width + int(spacing_ratio * usable_width)
    spacing_y = int(card_height * 0.40)
    y_inhabitant_offset = int(card_height * 0.12)

    inhabitant_width = int(card_width * 0.70)
    inhabitant_height = int(inhabitant_width * 1.4)

    for i, slot in enumerate(state.shop):
        nb_locations = len(slot.locations)
        inhabitant_x = x_offset + i * spacing_x + (card_width - inhabitant_width) // 2
        if nb_locations > 0:
            inhabitant_y = y_offset + (nb_locations - 1) * spacing_y + card_height + y_inhabitant_offset
        else:
            inhabitant_y = y_offset + card_height + y_inhabitant_offset

        inhabitant: Inhabitant | None = slot.inhabitant
        if inhabitant is not None and hasattr(inhabitant, "image_path"):
            try:
                img = pygame.image.load(inhabitant.image_path)
                img = pygame.transform.scale(img, (inhabitant_width, inhabitant_height))
                screen.blit(img, (inhabitant_x, inhabitant_y))
            except FileNotFoundError:
                pygame.draw.rect(screen, (70, 70, 140), (inhabitant_x, inhabitant_y, inhabitant_width, inhabitant_height))
                err = font.render("Image ?", True, (255, 0, 0))
                err_x = inhabitant_x + inhabitant_width // 8
                err_y = inhabitant_y + inhabitant_height // 2 - 10
                screen.blit(err, (err_x, err_y))
        elif inhabitant is not None:
            pygame.draw.rect(screen, (70, 70, 140), (inhabitant_x, inhabitant_y, inhabitant_width, inhabitant_height))
            label = font.render(f"{type(inhabitant).__name__}", True, (255, 255, 255))
            label_x = inhabitant_x + 10
            label_y = inhabitant_y + inhabitant_height // 2 - 10
            screen.blit(label, (label_x, label_y))