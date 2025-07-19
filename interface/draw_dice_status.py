import pygame
from game.gamestate import Game
from game.dice import Die, DiceColor

def draw_dice_status(state: Game, screen):
    font = pygame.font.SysFont(None, 26)

    width, height = screen.get_size()

    dice = state.die_roll.dice
    dice_count = len(dice)

    die_size = 50
    spacing = 20
    total_width = dice_count * die_size + (dice_count - 1) * spacing
    start_x = (width - total_width) // 2
    y = height - 80  # Position à 80 px du bas

    for i, die in enumerate(dice):
        result, color = die.currentResult
        x = start_x + i * (die_size + spacing)

        # Couleur associée au dé
        if color == DiceColor.RED:
            die_color = (200, 50, 50)
        elif color == DiceColor.GREEN:
            die_color = (50, 180, 50)
        elif color == DiceColor.BLUE:
            die_color = (50, 100, 200)
        else:
            die_color = (150, 150, 150)

        # Dessine un carré pour le dé
        pygame.draw.rect(screen, die_color, (x, y, die_size, die_size), border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, die_size, die_size), 2, border_radius=5)

        # Affiche le chiffre au centre du dé
        text_surf = font.render(str(result), True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(x + die_size // 2, y + die_size // 2))
        screen.blit(text_surf, text_rect)

    # Affiche le nombre de relances
    roll_font = pygame.font.SysFont(None, 22)
    tries_text = roll_font.render(f"Relance : {state.die_roll.nb_tries-1}/2", True, (255, 255, 0))
    screen.blit(tries_text, (start_x, y - 30))
