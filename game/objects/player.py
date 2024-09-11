import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,competences,etoile,country,images):
        super().__init__()
        self.image_index = 0
        self.images = images
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vitesse = 3
        self.competences = competences
        self.etoile = etoile
        self.country = country
        self.animation_speed = 2
        self.animation_counter = 0
    #more test
    def update(self):
        self.hitbox.center = self.rect.center

    def deplacer(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x >0:
            self.rect.x -= self.vitesse
            self.animer(2,3)
        elif keys[pygame.K_RIGHT]and self.rect.x <1000:
            self.rect.x += self.vitesse
            self.animer(4,5)
        elif keys[pygame.K_UP]and self.rect.y >0:
            self.rect.y -= self.vitesse
            self.animer(6,7)
        elif keys[pygame.K_DOWN]and self.rect.y <744:
            self.rect.y += self.vitesse
            self.animer(0,1)
    def animer(self,index1,index2):
        self.animation_speed = 2
        self.animation_counter += 1
        images_anim = [self.images[index1],self.images[index2]]
        if self.animation_counter >= self.animation_speed:
            self.image_index = (self.image_index + 1) % len(images_anim)
            self.image = images_anim[self.image_index]
            self.image = pygame.transform.scale(self.image,(32,32))
            self.animation_counter = 0




