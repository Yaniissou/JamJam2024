import os
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, competences):
        super().__init__()
        # Utilisation d'un chemin absolu pour charger l'image
        current_dir = os.path.dirname(__file__)
        self.image = pygame.image.load(os.path.join(current_dir, "../assets/tile000.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = 3
        self.competences = competences

    def dessiner(self, fenetre):
        fenetre.blit(self.image, self.rect)

    def deplacer(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.vitesse
        if keys[pygame.K_RIGHT] and self.rect.x < 1024 - self.rect.width:  # Limite à 1024 (la largeur de la fenêtre)
            self.rect.x += self.vitesse
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.vitesse
        if keys[pygame.K_DOWN] and self.rect.y < 768 - self.rect.height:  # Limite à 768 (la hauteur de la fenêtre)
            self.rect.y += self.vitesse
