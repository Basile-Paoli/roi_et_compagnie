import pygame
from game.gamestate import Game
from game.card_types import Location

def draw_locations(state: Game, screen):
    font = pygame.font.SysFont(None, 24)
    
    x_offset = 20
    y_offset = 30
    spacing_x = 180
    spacing_y = 60
    label_y_offset = 40

    for i, slot in enumerate(state.shop):
        # On dessine les emplacements de location restants du slot
        for j, location in enumerate(slot.locations):
            if isinstance(location, Location):
                try:
                    image = pygame.image.load(location.image_path)
                    image = pygame.transform.scale(image, (170, 110))
                    screen.blit(image, (x_offset + i * spacing_x, y_offset + j * spacing_y))
                except FileNotFoundError:
                    print(f"Image non trouvée : {location.image_path}")

        label = font.render(slot.type.name, True, (255, 255, 255))
        
        if len(slot.locations) > 0:
            dernier_y = y_offset + (len(slot.locations) - 1) * spacing_y
            text_y = dernier_y + 110 + 8
        else:
            text_y = y_offset

        screen.blit(label, (x_offset + i * spacing_x, text_y))
