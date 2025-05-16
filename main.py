import pygame
from pygame.surface import Surface
from pygame import display
from pygame.rect import Rect


# Temporary main function to test out pygame. We should in the future have a client.py file and a server.py file as entrypoints.
def main() -> None:
    pygame.init()

    screen: Surface = display.set_mode((800, 600))
    display.set_caption("My Game")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        rectangle: Rect = Rect(100, 100, 50, 50)

        surf: Surface = Surface((50, 50))
        surf.fill((255, 0, 0))


        screen.fill((0, 0, 0))
        screen.blit(surf, rectangle)
        display.flip()

if __name__ == "__main__":
    main()
