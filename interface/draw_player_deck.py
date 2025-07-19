import pygame
from game.card_types import Location, Penalty
from game.inhabitant import Inhabitant
from game.gamestate import Player

def draw_player_deck(player: Player, screen, y_offset=400):
    x_offset = 20
    spacing_x = 110

    for i, card in enumerate(player.kingdom):
        x = x_offset + i * spacing_x
        if hasattr(card, "image_path"):
            try:
                image = pygame.image.load(card.image_path)
                image = pygame.transform.scale(image, (100, 140))  # Taille fixe
                screen.blit(image, (x, y_offset))
            except FileNotFoundError:
                print(f"Image non trouvée : {card.image_path}")
        else:
            # Affichage simplifié si pas d’image
            pygame.draw.rect(screen, (255, 0, 0), (x, y_offset, 100, 140))

    font = pygame.font.SysFont(None, 28)
    label = font.render(f"Royaume de Joueur {player.id + 1}", True, (255, 255, 255))
    screen.blit(label, (20, y_offset - 30))
