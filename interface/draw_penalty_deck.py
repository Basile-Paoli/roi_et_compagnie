import pygame
from game.card_types import Penalty
from game.gamestate import Game

import pygame
from game.card_types import Penalty


def draw_penalty_deck(state: Game, screen, screen_width=1200, x_offset=50, y_offset=50):
    """Affiche seulement la carte du dessus du deck de pénalités."""
    card_width, card_height = 110, 150
    pile_x = screen_width - x_offset - card_width  # Position à droite de l'écran
    pile_y = y_offset

    if len(state.penalty_deck) > 0:
        # On prend uniquement la première carte de la pile (côté joueur : visuellement "le dessus")
        penalty = state.penalty_deck[-1]
        if hasattr(penalty, "image_path"):
            try:
                image = pygame.image.load(penalty.image_path)
                image = pygame.transform.scale(image, (card_width, card_height))
                screen.blit(image, (pile_x, pile_y))
            except FileNotFoundError:
                pygame.draw.rect(screen, (180, 0, 0), (pile_x, pile_y, card_width, card_height))
        else:
            pygame.draw.rect(screen, (180, 0, 0), (pile_x, pile_y, card_width, card_height))
    else:
        # Si pile vide
        font_small = pygame.font.SysFont(None, 20)
        aucun_label = font_small.render("Pioche vide", True, (255, 255, 255))
        screen.blit(aucun_label, (pile_x, pile_y + 10))

