import time
import random

import pygame


class QTE:
    def __init__(self, duree,isFinish,images):
        self.duree = duree #int
        self.isFinish = isFinish
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


        self.image_index = 0
        self.images = images
        self.image = self.images[self.image_index]
        self.animation_speed = 2
        self.animation_counter = 0

    def start(self,window_width,window_height,color,screen, font, player):

        if not self.isFinish:
            self.animer(window_width,window_height,screen)
            letter = font.render(self.letter, False, (0,0,0))
            letter_rect = letter.get_rect(center=(window_width/2, window_height/2))
            screen.blit(letter, letter_rect)

            if pygame.key.get_pressed()[self.key] == True and not self.pressed:
                print("on a checké la bonne key")
                self.pressed = True
                self.updateLetter()
                player.etoile += 5


        if self.isFinish:
            self.isFinish = False


    def onEnd(self):
        print('fin!');

    def updateLetter(self):
        self.letter = random.choice(list(self.keys.keys()))
        self.key = self.keys[self.letter]
        self.pressed = False
    def animer(self,window_width,window_height,screen):

        self.animation_speed = 8
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            self.animation_counter = 0
        self.image = pygame.transform.scale(self.image,(window_width/2, window_height/2))
        screen.blit(self.image, ((window_width - self.image.get_width()) // 2, (window_height - self.image.get_height()) // 2))

