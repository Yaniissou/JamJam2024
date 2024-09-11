import random

import pygame
import time
from game.objects.QTE import QTE

class ClicGame(QTE):
    def __init__(self, duree, action, screen):
        QTE.__init__(self, duree, action, screen)
        self.score = 0

    def start(self):


        while self.timeLeft() > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si le joueur clique sur la cible
                    if self.target_rect and self.target_rect.collidepoint(event.pos):
                        print("Cible touchée!")
                        self.score += 1
                        self.create_target()  # Créer une nouvelle cible

        print("Temps écoulé")
        self.onEnd()

    def onEnd(self):
        print('fin! score: ', self.score)

    def timeLeft(self):
        return self.timestamp + self.duree - int(time.time())

    def create_window(self):
        self.screen.fill((255, 255, 255))  # Efface l'écran
        pygame.draw.rect(self.screen, (0, 0, 0), (150, 100, 400, 300))  # Dessiner la fenêtre
        self.create_target()

    def create_target(self):
        target_x = random.randint(160, 520)
        target_y = random.randint(110, 380)
        self.target_rect = pygame.Rect(target_x, target_y, 30, 30)  # Crée un rectangle pour la cible

    def update_window(self):
        self.screen.fill((255, 255, 255))  # Effacer l'écran (optionnel)
        pygame.draw.rect(self.screen, (0, 0, 0), (150, 100, 400, 300))  # Redessiner la fenêtre
        pygame.draw.rect(self.screen, (255, 0, 0), self.target_rect)  # Dessiner la cible

        # Afficher le score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (200, 110))

        pygame.display.flip()