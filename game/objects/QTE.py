import time
import pygame

class QTE:
    def __init__(self, duree, action, screen):
        self.duree = duree #int
        self.action = action #event
        self.screen = screen #affichage du qte
        self.timestamp = int(time.time())
        print(self.timestamp)
        self.start()

    #fonction qui s'exécute à la fin du qte
    def start(self):


        while time.time() <= (self.timestamp + self.duree):
            print(time.time())
            # on détecte les events
            for event in pygame.event.get():
                # si l'event correspond à ce qu'on doit faire
                if event.type == self.action:
                    # on annule le qte
                    print("c'est bon!!!")
                    return


        # Si on atteint cet endroit, le temps est écoulé
        print("Temps écoulé")

    def onEnd(self):
        print('fin!');


