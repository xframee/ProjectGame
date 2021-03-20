import pygame
import sys
import os
import pytmx
from settings import *



class Game:
    def __init__ (self):
        pygame.init()
        os.chdir("/Users/alissahansen/Documents/GitHub/ProjectGame")
        self.playerImage = pygame.image.load('player1.png')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        pygame.key.set_repeat(100, 100)

        self.cameraX = 0
        self.cameraY = 0
        self.playerX = 10  
        self.playerY = 10

    def setup(self):
      pass  

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
        pass
    
    def drawToScreen(self):
        gameMap = pytmx.load_pygame('map2.tmx')
        for layer in gameMap.visible_layers:
            for x, y, gid, in layer:
                tile = gameMap.get_tile_image_by_gid(gid)
                if(tile):
                    self.screen.blit(tile, (x * gameMap.tilewidth, y * gameMap.tileheight))
        self.screen.blit(self.playerImage, (self.playerX, self.playerY))
        pygame.display.flip() # Flip til sidst for optimering

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: 
                    self.quit()
                if event.key == pygame.K_a:
                    self.playerX -= 5
                if event.key == pygame.K_d:
                    self.playerX += 5
                if event.key == pygame.K_w:
                    self.playerY -= 5
                if event.key == pygame.K_s:
                    self.playerY += 5
    
    def startScreen(self):
        pass
    
    
g = Game()
while True:
    g.running()     

 