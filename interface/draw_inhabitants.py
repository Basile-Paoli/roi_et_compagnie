from game.inhabitant import Inhabitant
from game.gamestate import Game
import pygame

def draw_inhabitants(state: Game, screen):
    font = pygame.font.SysFont(None, 20)
    x_offset = 20
    base_y = 30
    spacing_x = 180
    spacing_loc = 30
    height_loc = 110  # hauteur de l'image location
    y_inhabitant_offset = 20  # décalage sous la dernière location

    for i, slot in enumerate(state.shop):
        # Trouver la position Y pour l'habitant, sous la dernière carte location affichée
        y_of_inhabitant = base_y + len(slot.locations) * spacing_loc + height_loc + y_inhabitant_offset

        inhabitant: Inhabitant | None = slot.inhabitant
        if inhabitant is not None and hasattr(inhabitant, "image_path"):
            try:
                img = pygame.image.load(inhabitant.image_path)
                img = pygame.transform.scale(img, (80, 110))
                screen.blit(img, (x_offset + i * spacing_x + 45, y_of_inhabitant))  # léger centrage
            except FileNotFoundError:
                pygame.draw.rect(screen, (70, 70, 140), (x_offset + i * spacing_x + 45, y_of_inhabitant, 80, 110))
                err = font.render("Image ?", True, (255, 0, 0))
                print(inhabitant.image_path)
                screen.blit(err, (x_offset + i * spacing_x + 55, y_of_inhabitant + 40))
        elif inhabitant is not None:
            # Pas d'image, juste une boîte
            pygame.draw.rect(screen, (70, 70, 140), (x_offset + i * spacing_x + 45, y_of_inhabitant, 80, 110))
            label = font.render(f"{type(inhabitant).__name__}", True, (255, 255, 255))
            screen.blit(label, (x_offset + i * spacing_x + 55, y_of_inhabitant + 40))



def draw_inhabitants_2(state: Game, screen):
    font = pygame.font.SysFont(None, 20)
    x_offset = 20
    y_offset = 230   # adapte ce Y pour bien placer la ligne sous les autres cartes si besoin
    spacing_x = 180  # même espacement que le shop
    card_width = 80
    card_height = 110

    font = pygame.font.SysFont(None, 20)
    x_offset = 20
    base_y = 30
    spacing_x = 180
    spacing_loc = 30
    height_loc = 110  # hauteur de l'image location
    y_inhabitant_offset = 20  # décalage sous la dernière location

    for i, slot in enumerate(state.shop):
        # Trouver la position Y pour l'habitant, sous la dernière carte location affichée
        y_of_inhabitant = base_y + len(slot.locations) * spacing_loc + height_loc + y_inhabitant_offset

        inhabitant: Inhabitant | None = slot.inhabitant
        if inhabitant is not None and hasattr(inhabitant, "image_path"):
            try:
                img = pygame.image.load(inhabitant.image_path)
                img = pygame.transform.scale(img, (80, 110))
                screen.blit(img, (x_offset + i * spacing_x + 45, y_of_inhabitant))  # léger centrage
            except FileNotFoundError:
                pygame.draw.rect(screen, (70, 70, 140), (x_offset + i * spacing_x + 45, y_of_inhabitant, 80, 110))
                err = font.render("Image ?", True, (255, 0, 0))
                print(inhabitant.image_path)
                screen.blit(err, (x_offset + i * spacing_x + 55, y_of_inhabitant + 40))
        elif inhabitant is not None:
            # Pas d'image, juste une boîte
            pygame.draw.rect(screen, (70, 70, 140), (x_offset + i * spacing_x + 45, y_of_inhabitant, 80, 110))
            label = font.render(f"{type(inhabitant).__name__}", True, (255, 255, 255))
            screen.blit(label, (x_offset + i * spacing_x + 55, y_of_inhabitant + 40))