import pygame
from typing import List, Tuple
from game.gamestate import Player

def draw_dragon_selection_overlay(screen: pygame.Surface, possible_targets: List[Player] ) -> List[Tuple[pygame.Rect, Player]]:
    """
    Dessine la surimpression de sélection du joueur à qui donner le dragon.
    Retourne la liste des tuples (rect, Player) pour la détection du clic.
    """
    width, height = screen.get_size()

    # Assombrir le fond
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill((0,0,0,180))
    screen.blit(s,(0,0))
    
    font = pygame.font.SysFont(None, 40)
    text = font.render("À qui donner le Dragon ?", True, (255, 220, 50))
    screen.blit(text, (width//2 - text.get_width()//2, 40))
    
    button_font = pygame.font.SysFont(None, 30)
    btn_w, btn_h = 230, 48
    spacing = 20
    start_y = 120
    rects: List[Tuple[pygame.Rect, Player]] = []
    for i, p in enumerate(possible_targets):
        btn_x = width//2 - btn_w//2
        btn_y = start_y + i * (btn_h + spacing)
        r = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        rects.append((r, p))
        pygame.draw.rect(screen, (90,120,255), r, border_radius=6)
        label = button_font.render(f"Joueur {p.id+1}", True, (0,0,50))
        screen.blit(label, (btn_x + 24, btn_y + 8))
    return rects