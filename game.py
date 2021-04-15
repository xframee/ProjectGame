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
        os.chdir(r"C:\Users\Bandit\Desktop\RUC\Kurser\SD\ProjectGame")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        pygame.key.set_repeat(20, 100)
        self.setup()

    def setup(self):
        self.map = TiledMap('map2.tmx')
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.pytmx_map = pytmx.load_pygame('map2.tmx')

    def newSprite(self):
        self.all_sprites = pygame.sprite.Group()
        self.camera = Camera(self.map.width, self.map.height)
        self.player = Player(self, 400, 70)

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
        self.camera.update(self.player)
    

    def drawToScreen(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip() # Flip til sidst for optimering
     

    def events(self):
           
        for layer in self.pytmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "Trees_left":
                    for obj in layer:
                        if pygame.Rect (obj.x, obj.y, obj.width, obj.height).colliderect(self.player.rect) == True:
                            print ("Træ venstre")
                            break

                if layer.name == "Trees_top":
                    for obj in layer:
                        if pygame.Rect (obj.x, obj.y, obj.width, obj.height).colliderect(self.player.rect) == True:
                            print ("Træ top")
                            break

                if layer.name == "Trees_right":
                    for obj in layer:
                        if pygame.Rect (obj.x, obj.y, obj.width, obj.height).colliderect(self.player.rect) == True:
                            print ("Træ Højre")
                            break

                if layer.name == "Trees_bottom":
                    for obj in layer:
                        if pygame.Rect (obj.x, obj.y, obj.width, obj.height).colliderect(self.player.rect) == True:
                            print ("Træ Nede")
                            break

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
