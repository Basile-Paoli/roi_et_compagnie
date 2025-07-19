import pygame
from game.gamestate import Game
from game.card_types import Location

def draw_locations(state: Game, screen):
    font = pygame.font.SysFont(None, 24)

    width, height = screen.get_size()

    usable_width = width * 0.80
    shop_count = max(len(state.shop), 1)
    spacing_ratio = 0.04
    total_spacing = (shop_count + 1) * spacing_ratio * usable_width
    card_width = int((usable_width - total_spacing) / shop_count)
    card_height = int(card_width / 1.5)

    x_offset = int(width * 0.02)
    y_offset = int(height * 0.03)
    spacing_x = card_width + int(spacing_ratio * usable_width)
    spacing_y = int(card_height * 0.30)
    label_y_offset = int(card_height * 0.08)

    for i, slot in enumerate(state.shop):
        for j, location in enumerate(slot.locations):
            if isinstance(location, Location):
                try:
                    image = pygame.image.load(location.image_path)
                    image = pygame.transform.scale(image, (card_width, card_height))
                    pos_x = x_offset + i * spacing_x
                    pos_y = y_offset + j * spacing_y
                    screen.blit(image, (pos_x, pos_y))
                except FileNotFoundError:
                    print(f"Image non trouvée : {location.image_path}")

        label = font.render(slot.type.name, True, (255, 255, 255))
        if len(slot.locations) > 0:
            dernier_y = y_offset + (len(slot.locations) - 1) * spacing_y
            text_y = dernier_y + card_height + label_y_offset
        else:
            text_y = y_offset
        label_x = x_offset + i * spacing_x
        screen.blit(label, (label_x, text_y))