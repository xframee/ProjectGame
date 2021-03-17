import pygame
import sys
from sprites import *
from settings import *

class Game:
    def __init__ (self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        pygame.key.set_repeat(100, 100)

    def setup(self):
        pass 

    def newSprite(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self, 5, 5)

    def running (self):
        self.running = True
        while self.running: 
            self.events()
            self.update()
            self.drawToScreen()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()    

    def grid (self):
        for x in range (0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, RED, (x, 0), (x, HEIGHT))
        for y in range (0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, RED, (0, y) , (WIDTH, y))

    def drawToScreen(self):
        self.screen.fill(BLACK)
        self.grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip() # Flip til sidst for optimering

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: 
                    self.quit()
                if event.key == pygame.K_a:
                    self.player.move(dx=-1)
                if event.key == pygame.K_d:
                    self.player.move(dx=+1)
                if event.key == pygame.K_w:
                    self.player.move(dy=-1)
                if event.key == pygame.K_s:
                    self.player.move(dy=+1)
    
    def startScreen(self):
        pass
    
    
g = Game()
while True:
    g.newSprite()
    g.running()     

 