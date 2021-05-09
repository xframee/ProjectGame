import pygame
import sys
import os
import pytmx
import random
from sprites import *
from settings import *
from camera import *

class Game:

    def __init__ (self):
        pygame.init()
        #os.chdir("/Users/alissahansen/Documents/GitHub/ProjectGame") 
        os.chdir(r"C:\Users\Bandit\Desktop\RUC\Kurser\SD\ProjectGame")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(10, 100)
        self.setup()

    def setup(self):
        self.map = TiledMap('map2.tmx')
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.pytmx_map = pytmx.load_pygame('map2.tmx')
        self.points = 0

    def newSprite(self):
        self.all_sprites = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.camera = Camera(self.map.width, self.map.height)
        self.player = Player(self, 400, 70)
        for x in range(3):
            self.enemy = Enemy(self, random.randint(TILESIZE, (3200-TILESIZE)), 
            random.randint(TILESIZE, (1920-TILESIZE)))

    def running (self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 
            self.events()
            self.update()
            self.drawToScreen()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        #Nedenfor tjekker om enemy rammer player
        isPlayerHit = pygame.sprite.groupcollide(self.playerGroup, self.mobs, False, False) 
        for hit in isPlayerHit:
            self.player.health -= PROJECTILE_DAMAGE
            print(self.player.health)

        #Nedenfor tjekker for kollision mellem skud og enemies
        isEnemyHit = pygame.sprite.groupcollide(self.mobs, self.projectiles, False, True) 
        #false for mobs, da et mob ikke skal forsvinde, når de bliver ramt af et skud, 
        # men et skud skal forsvinde, når det rammer et mob, derfor true. 
        for hit in isEnemyHit:
            hit.health -= PROJECTILE_DAMAGE
            hit.vel = vec(0, 0)
            self.points += PLAYER_POINTS
        
    def drawToScreen(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.drawHealth()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip() # Flip til sidst for optimering
     
#Hit detection for the player model
    def hitDetectionLeftTrees(self, SpriteToCheck):
        for layer in self.pytmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "Trees_left":
                    for obj in layer:
                        return pygame.Rect (obj.x, obj.y, obj.width, obj.height).colliderect(SpriteToCheck)
                
    def hitDetectionTopTrees(self, SpriteToCheck):
        for layer in self.pytmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "Trees_top":
                    for obj in layer:
                        return pygame.Rect (obj.x, obj.y, obj.width, obj.height).colliderect(SpriteToCheck)


    def hitDetectionRightTrees(self, SpriteToCheck):
        for layer in self.pytmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "Trees_right":
                    for obj in layer:
                        return pygame.Rect (obj.x, obj.y, obj.width, obj.height).colliderect(SpriteToCheck)

    def hitDetectionBottomTrees(self, SpriteToCheck):
        for layer in self.pytmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "Trees_bottom":
                    for obj in layer:
                        return pygame.Rect (obj.x, obj.y, obj.width, obj.height).colliderect(SpriteToCheck)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: 
                    self.quit()
    
    def startScreen(self):
        pass
        #Create greeting screen
    
    def gameOver(self):
        pass
        #Create gameover screen
    
g = Game()
while True:
    g.newSprite()
    g.running()