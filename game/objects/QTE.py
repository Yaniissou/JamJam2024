import time
import random

import pygame


class QTE:
    def __init__(self, duree,isFinish):
        self.duree = duree #int
        self.isFinish = isFinish
        self.wons = 0
        self.keys = {
            "a": pygame.K_a,
            "b": pygame.K_b,
            "c": pygame.K_c,
            "d": pygame.K_d,
            "e": pygame.K_e,
            "f": pygame.K_f,
            "g": pygame.K_g,
            "h": pygame.K_h,
            "i": pygame.K_i,
            "j": pygame.K_j,
            "k": pygame.K_k,
            "l": pygame.K_l,
            "m": pygame.K_m,
            "n": pygame.K_n,
            "o": pygame.K_o,
            "p": pygame.K_p,
            "q": pygame.K_q,
            "r": pygame.K_r,
            "s": pygame.K_s,
            "t": pygame.K_t,
            "u": pygame.K_u,
            "v": pygame.K_v,
            "w": pygame.K_w,
            "x": pygame.K_x,
            "y": pygame.K_y,
            "z": pygame.K_z,
            "space": pygame.K_SPACE,
            "enter": pygame.K_RETURN,
        }
        self.updateLetter()
        self.pressed = False



    def start(self,window_width,window_height,color,screen, font):

        if not self.isFinish:
            pygame.draw.rect(screen,color,(window_width/4, window_height/4,window_width/2, window_height/2))

            letter = font.render(self.letter, False, (0,0,0))
            letter_rect = letter.get_rect(center=(window_width/2, window_height/2))
            screen.blit(letter, letter_rect)
            #print(pygame.key.get_pressed())

            if pygame.key.get_pressed()[self.key] == True and not self.pressed:
                print("on a checké la bonne key")
                self.pressed = True
                self.updateLetter()
                self.wons += 1

        if self.isFinish:
            self.isFinish = False


    def onEnd(self):
        print('fin!');

    def updateLetter(self):
        self.letter = random.choice(list(self.keys.keys()))
        self.key = self.keys[self.letter]
        self.pressed = False
