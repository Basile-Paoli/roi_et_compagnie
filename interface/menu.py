import pygame

def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 48)
    options = [1, 2, 3, 4]
    selected = 0
    running = True

    while running:
        screen.fill((30, 30, 30))
        title = font.render("Sélection du nombre de joueurs", True, (255, 255, 255))
        screen.blit(title, (100, 100))

        for i, nb in enumerate(options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            text = font.render(f"{nb} joueur{'s' if nb > 1 else ''}", True, color)
            screen.blit(text, (150, 200 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    return options[selected]