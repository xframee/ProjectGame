import pygame
import sys
from sprites import *
from settings import *

class Game:
    def __init__ (self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

    def setup(self):
        pass

    def running (self):
        running = True
        while running: 
            self.events()

    def quit(self):
        pygame.quit()
        sys.exit()

    def grid (self):
        for x in range (0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen)
        for y in range (0, HEIGHT, TILESIZE):
            pass

    def drawToScreen(self):
        pygame.display.flip() # Flip til sidst for optimering

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: 
                    self.quit()
    
    def startScreen(self):
        pass
    
    
g = Game()
while True:
    g.running()     

 