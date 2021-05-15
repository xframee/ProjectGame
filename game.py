import pygame
import sys
import os
from pygame import draw
import pytmx
import random
from sprites import * 
from settings import *
from camera import *

#HUD
def drawPLayerHealth (surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

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
        self.score_string = f"Score: {self.points}"

    def newSprite(self):
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        self.camera = Camera(self.map.width, self.map.height)
        self.player = Player(self, 400, 70)
        for x in range(3):
            self.enemy = Enemy(self, random.randint(TILESIZE + 10, (3200-(TILESIZE + 10))), 
            random.randint(TILESIZE + 10, (1920-(TILESIZE + 10))))

    def running (self):
        self.playing = True
        while self.playing:
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
        isPlayerHit = pygame.sprite.groupcollide(self.mobs, self.player_group, False, False) 
        for hit in isPlayerHit:
            hit.vel = vec(0, 0) #Gør så den enemy der skader playeren ikke bevæger sig lige efterw
            if self.player.canTakeDamage(): #Tjekker om der er gået tid mellem sidste slag og nyt slag
                self.player.health -= ENEMY_DAMAGE
                if self.player.health <= 0:
                    self.playing = False

        #Nedenfor tjekker for kollision mellem skud og enemies
        isEnemyHit = pygame.sprite.groupcollide(self.mobs, self.projectiles, False, True) 
        #false for mobs, da et mob ikke skal forsvinde, når de bliver ramt af et skud, 
        # men et skud skal forsvinde, når det rammer et mob, derfor true. 
        for hit in isEnemyHit:
            hit.health -= PROJECTILE_DAMAGE
            hit.vel = vec(0, 0)
            self.points += PLAYER_POINTS
            self.score_string = f"Score: {self.points}"
        
    def drawToScreen(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.drawHealth()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #Draw HUD
        drawPLayerHealth(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.drawText(self.screen, self.score_string, 18 , 1300, 65)
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

    # Fuction til at lave tekst på skærmen
    def drawText (self, surf, text, size, x, y):
        font = pygame.font.Font(FONT_NAME, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surf.blit(text_surface, text_rect)

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
        self.points = 0
        self.score_string = f"Score: {self.points}"
        #Create gameover screen
    
g = Game()
g.startScreen()
while True:
    g.newSprite()
    g.running()
    g.gameOver()