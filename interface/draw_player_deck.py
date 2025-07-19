import pygame
from game.card_types import Location, Penalty
from game.inhabitant import Inhabitant
from game.gamestate import Player

def draw_player_deck(player, screen):
    width, height = screen.get_size()

    # Panel à gauche (20% de la largeur, bas de l'écran)
    card_left_ratio = 0.20
    panel_left = int(width * 0.02)                         # petite marge à gauche
    panel_width = int(width * card_left_ratio)
    card_width = int(panel_width * 0.8)
    card_height = int(card_width * 1.4)                    # portrait (ajuste si besoin)

    # Position bas-gauche avec une petite marge en bas
    x = panel_left
    y = height - card_height - 32                          # 32 px pour le texte en dessous

    # Si le deck contient au moins une carte, affiche la carte du dessus
    if player.kingdom:
        card = player.kingdom[-1]
        if hasattr(card, "image_path"):
            try:
                image = pygame.image.load(card.image_path)
                image = pygame.transform.scale(image, (card_width, card_height))
                screen.blit(image, (x, y))
            except FileNotFoundError:
                pygame.draw.rect(screen, (255, 0, 0), (x, y, card_width, card_height), 3)  # error border
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, card_width, card_height), 3)
    else:
        # Deck vide : rectangle vide
        pygame.draw.rect(screen, (200, 200, 200), (x, y, card_width, card_height), 3)      # Bord gris clair[1][2][9]

    # Label ("Royaume de Joueur X") sous la carte
    font = pygame.font.SysFont(None, 22)
    label = font.render(f"Royaume de Joueur {player.id + 1}", True, (255, 255, 255))
    label_rect = label.get_rect(midtop=(x + card_width // 2, y + card_height + 6))
    screen.blit(label, label_rect)
