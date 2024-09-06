from threading import Timer
import pygame

class QTE:
    def __init__(self, duree, action, screen):
        self.duree = duree #int
        self.action = action #event
        self.screen = screen #affichage du qte


    #fonction qui s'exécute à la fin du qte
    def exec(self):
        #la clock (?)
        clock = pygame.time.Clock()
        #on affiche "fin" après que ça soit terminé
        timer = Timer(self.duree, print("fin"))
        #démarrer le timer du qte
        timer.start()

        #tant que le timer est actif
        while timer.is_alive():
            #on détecte les events
            for event in pygame.event.get():
                #si l'event correspond à ce qu'on doit faire
                if event.type == self.action:
                    #on annule le qte
                    timer.cancel()
                    print("c'est bon!!!")

        clock.tick(30)
        #actualiser visuel
        pygame.display.flip()




