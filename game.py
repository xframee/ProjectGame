import pygame
import sys
import os
import pytmx
from sprites import *
from settings import *
from camera import *


class Game:
    def __init__ (self):
        pygame.init()
        os.chdir("/Users/alissahansen/Documents/GitHub/ProjectGame")
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
    

    def drawToScreen(self):
        gameMap = pytmx.load_pygame('map2.tmx')
        for layer in gameMap.visible_layers:
            for x, y, gid, in layer:
                tile = gameMap.get_tile_image_by_gid(gid)
                if(tile):
                    self.screen.blit(tile, (x * gameMap.tilewidth, y * gameMap.tileheight))
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
                    self.player.move(dx=-10)
                if event.key == pygame.K_d:
                    self.player.move(dx=+10)
                if event.key == pygame.K_w:
                    self.player.move(dy=-10)
                if event.key == pygame.K_s:
                    self.player.move(dy=+10)
    
    def startScreen(self):
        pass
    
    
g = Game()
while True:
    g.newSprite()
    g.running()     

 