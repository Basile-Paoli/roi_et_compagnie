import pygame

def draw_button(screen, rect, text, font, bg_color, text_color=(255, 255, 255)):
    pygame.draw.rect(screen, bg_color, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # bordure blanche
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)