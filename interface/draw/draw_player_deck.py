import pygame
import collections

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

    font = pygame.font.SysFont(None, 24)
    line_height = font.get_linesize()

    # On compte chaque type de carte
    card_counter = collections.Counter()

    for card in player.kingdom:
        if isinstance(card, Inhabitant):
            card_type = type(card).__name__  # Par exemple "Gnome"
        elif isinstance(card, Location):
            card_type = type(card).__name__  # OU card.name si tu préfères le nom du lieu
        elif isinstance(card, Penalty):
            card_type = "Malus"
        else:
            card_type = "Carte inconnue"
        card_counter[card_type] += 1

    # On trie dans l'ordre alphabétique pour l'affichage
    card_lines = [f"{count} {name}{'s' if count>1 and not name.endswith('s') else ''}" for name, count in sorted(card_counter.items())]

    # Position du texte (à droite du deck)
    text_x = x + card_width + 18
    text_y = y

    # Affichage de chaque ligne (chaque type de carte)
    for i, line in enumerate(card_lines):
        text_surf = font.render(line, True, (255, 255, 255))
        screen.blit(text_surf, (text_x, text_y + i * line_height))
    
    # Total des points (juste après la liste)
    total_points = player.kingdom.total_value() if hasattr(player.kingdom, "total_value") else 0
    points_line = f"Points : {total_points}"
    text_surf = font.render(points_line, True, (255, 215, 0))
    screen.blit(text_surf, (text_x, text_y + len(card_lines) * line_height + 8))