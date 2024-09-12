import time
import pygame

class QTE:
    def __init__(self, duree):
        self.duree = duree #int



    #fonction qui s'exécute à la fin du qte
    def start(self,window_width,window_height,color,screen):
        pygame.draw.rect(screen,color,(window_width/4, window_height/4,window_width/2, window_height/2))
        # Si on atteint cet endroit, le temps est écoulé
        self.onEnd()

    def onEnd(self):
        print('fin!');

