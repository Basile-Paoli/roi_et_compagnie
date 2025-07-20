import pygame

def draw_player_switch_overlay(screen, player_id, title_txt=None) -> None:
    width, height = screen.get_size()
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill((30, 30, 30, 160))
    screen.blit(s, (0, 0))
    
    font = pygame.font.SysFont(None, 86, bold=True)
    if title_txt is None:
        title_txt = f"Joueur {player_id + 1}"
    t_surf = font.render(title_txt, True, (240, 216, 40))
    shadow = font.render(title_txt, True, (0, 0, 0))
    screen.blit(shadow, (width // 2 - shadow.get_width() // 2 + 3, height // 2 - shadow.get_height() // 2 + 3))
    screen.blit(t_surf, (width // 2 - t_surf.get_width() // 2, height // 2 - t_surf.get_height() // 2))
