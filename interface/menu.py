import pygame
import os

def menu() -> int:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 48)

    options = [2, 3, 4]
    has_save = os.path.isfile("gamestate.json")
    menu_options: list[tuple[str, int]] = []

    if has_save:
        menu_options.append(("Reprendre la partie", -1))
    for nb in options:
        menu_options.append((f"{nb} joueur{'s' if nb > 1 else ''}", nb))
    menu_options.append(("Quitter le jeu", -2))

    selected = 0
    running = True

    while running:
        screen.fill((30, 30, 30))
        title = font.render("Sélection du nombre de joueurs", True, (255, 255, 0))
        screen.blit(title, (100, 100))

        for i, (txt, _) in enumerate(menu_options):
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            text = font.render(txt, True, color)
            screen.blit(text, (150, 200 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    return menu_options[selected][1]

    return -2
