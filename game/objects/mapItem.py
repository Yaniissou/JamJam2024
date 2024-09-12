import pygame.transform


class MapItem:
    def __init__(self, x,y, image):
        self.image = pygame.transform.scale(image, (32,32))
        self.rect = self.image.get_rect(topleft=(x,y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        