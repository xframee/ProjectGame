import pygame
import sys

pygame.init()

displayWidth = 800
displayHeight = 600

screen = pygame.display.set_mode((displayWidth, displayHeight))

game_over = False

while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
