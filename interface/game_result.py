import pygame
import sys

def game_result(state):
    pygame.init()
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    
    width, height = 500, 100 + 70 * len(state.players)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Résultats de la partie")
    
    results = [
        (player.id, player.kingdom.total_value())
        for player in state.players
    ]
    results.sort(key=lambda x: x[1], reverse=True)
    
    running = True
    while running:
        screen.fill((30, 30, 30))
        
        title = font.render("Scores finaux", True, (255, 255, 0))
        screen.blit(title, (width//2 - title.get_width()//2, 30))
        
        for i, (pid, score) in enumerate(results):
            text = small_font.render(f"Joueur {pid}: {score} points", True, (255, 255, 255))
            screen.blit(text, (60, 100 + i*60))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    sys.exit()
