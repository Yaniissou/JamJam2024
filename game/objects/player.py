import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/tile000.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = 3

    def deplacer(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x >0:
            self.rect.x -= self.vitesse
        elif keys[pygame.K_RIGHT]and self.rect.x <1000:
            self.rect.x += self.vitesse
        elif keys[pygame.K_UP]and self.rect.y >0:
            self.rect.y -= self.vitesse
        elif keys[pygame.K_DOWN]and self.rect.y <744:
            self.rect.y += self.vitesse





