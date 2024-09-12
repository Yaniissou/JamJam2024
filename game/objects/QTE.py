import time
import pygame

class QTE:
    def __init__(self, duree,isFinish):
        self.duree = duree #int
        self.isFinish = isFinish


    #fonction qui s'exécute à la fin du qte
    def start(self,window_width,window_height,color,screen):

        if not self.isFinish:
            pygame.draw.rect(screen,color,(window_width/4, window_height/4,window_width/2, window_height/2))
            print("début d'un qte")
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('action effectuée')
                    return

        if self.isFinish:
            self.isFinish = False


    def onEnd(self):
        print('fin!');

