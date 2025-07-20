import pygame

_image_cache: dict[tuple[int, int], pygame.Surface] = {}

def get_card_image(path, size) -> pygame.Surface:
    key = (path, size)
    if key not in _image_cache:
        try:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, size)
            image = image.convert_alpha()
            _image_cache[key] = image
        except FileNotFoundError:
            print(f"Image non trouvée : {path}")
            surf = pygame.Surface(size)
            surf.fill((255, 0, 0))
            _image_cache[key] = surf
    return _image_cache[key]