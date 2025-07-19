import pygame
from game.gamestate import Game
from game.dice import Die, DiceColor

def draw_dice_status(state: Game, screen, selected_dice):
    font = pygame.font.SysFont(None, 26)
    width, height = screen.get_size()

    dice = state.die_roll.dice
    dice_count = len(dice)

    die_size = 50
    spacing = 20
    total_width = dice_count * die_size + (dice_count - 1) * spacing
    start_x = (width - total_width) // 2
    y = height - 80

    die_rects = []

    for i, die in enumerate(dice):
        result, color = die.currentResult
        x = start_x + i * (die_size + spacing)
        rect = pygame.Rect(x, y, die_size, die_size)
        die_rects.append(rect)

        if color == DiceColor.RED:
            die_color = (200, 50, 50)
        elif color == DiceColor.GREEN:
            die_color = (50, 180, 50)
        elif color == DiceColor.BLUE:
            die_color = (50, 100, 200)
        else:
            die_color = (150, 150, 150)

        pygame.draw.rect(screen, die_color, rect, border_radius=5)

        
        border_color = (255, 255, 0) if i in selected_dice else (255, 255, 255)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=5)

        
        text_surf = font.render(str(result), True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    
    roll_font = pygame.font.SysFont(None, 22)
    tries_text = roll_font.render(f"Relance : {state.die_roll.nb_tries}/3", True, (255, 255, 0))
    screen.blit(tries_text, (start_x, y - 30))

    instruction_font = pygame.font.SysFont(None, 20)
    instruction = instruction_font.render("Cliquez sur les dés à relancer (aucun = tous)", True, (200, 200, 200))
    screen.blit(instruction, (start_x, y - 50))

    return die_rects
