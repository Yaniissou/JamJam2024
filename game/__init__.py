import pygame
from objects import GameState

pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
running = True
dt = 0
gamestate = GameState.GameState.ENTRYPOINT
window = pygame.display.set_mode((1024, 768))
background = pygame.image.load("../assets/menu-background.png")
while running:
    if gamestate == GameState.GameState.ENTRYPOINT:
        clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.blit(background, (0, 0))
    pygame.display.update()