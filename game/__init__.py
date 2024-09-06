import pygame
from objects import GameState
from objects.player import Player
from objects.button import Button


pygame.init()
window_width = 1024
window_height = 768
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0
gamestate = GameState.GameState.ENTRYPOINT
window = pygame.display.set_mode((window_width, window_height))
player = Player(1200,1200)
player.image = pygame.transform.scale(player.image, (100, 100))
titlefont = pygame.font.Font("./assets/fonts/RETROTECH.ttf", 72)

def initMenu():
    background = pygame.image.load("./assets/menu-background.png")

    titletext = titlefont.render("Concorde", False, (0, 0, 0))
    titletext_rect = titletext.get_rect()
    titletext_rect.center = (window_width/2, window_height/4)

    playbutton = Button()
    window.blit(background, (0, 0))
    window.blit(titletext, titletext_rect)

while running:
    if gamestate == GameState.GameState.ENTRYPOINT:
        clock.tick(60)
        initMenu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.deplacer()

    window.blit(player.image, player.rect)
    pygame.display.update()