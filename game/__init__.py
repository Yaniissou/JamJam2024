import pygame
from objects import GameState
from objects.player import Player
pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
running = True
dt = 0
gamestate = GameState.GameState.ENTRYPOINT
window = pygame.display.set_mode((1024, 768))
background = pygame.image.load("../assets/menu-background.png")
player = Player(1200,1200)
player.image = pygame.transform.scale(player.image, (100, 100))
while running:
    if gamestate == GameState.GameState.ENTRYPOINT:
        clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.deplacer()
    window.blit(background, (0, 0))
    window.blit(player.image, player.rect)
    pygame.display.update()
