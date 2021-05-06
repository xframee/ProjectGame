import pygame
from settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.vel = vec (0,0) #Velocity
        self.pos = vec (x,y) #Position
        self.game = game
        self.image = pygame.image.load('player1.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def get_keys(self):
        self.vel = vec (0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not self.game.hitDetectionLeftTrees():
            self.vel.x = -PLAYER_SPEED 
        if keys[pygame.K_d] and not self.game.hitDetectionRightTrees():
            self.vel.x = PLAYER_SPEED
        if keys[pygame.K_w] and not self.game.hitDetectionTopTrees():
            self.vel.y = -PLAYER_SPEED
        if keys[pygame.K_s] and not self.game.hitDetectionBottomTrees():
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('enemy1.png')
        self.rect = self.image.get_rect()
        self.pos = vec (x, y)
        self.vel = vec (0, 0)
        self.acc = vec (0, 0) #Acceleration
        self.image.set_colorkey(BLACK)
        self.rot = 0
        
    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec (MOB_SPEED, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt

        if (self.game.hitDetectionTopTreesEnemy() or self.game.hitDetectionLeftTreesEnemy() 
        or self.game.hitDetectionRightTreesEnemy() or self.game.hitDetectionBottomTreesEnemy()):
            self.vel = vec (0,0)
            
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2 #Equation of motion https://www.youtube.com/watch?v=SAbxZDBJX4E&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i&index=8&ab_channel=KidsCanCode
        self.rect.center = self.pos

class Projectile (pygame.sprite.Sprite):
    def __init__ (self, game, pos, dir):
        self.groups = game.all_sprites, game.projectiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load('PlayerProjectile.png')
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * PROJECTILE_SPEED #Projektilet bruger en retningsvektor for at finde retningen den skal skydes i og ganger denne med farten
        self.spawnTime = pygame.time.get_ticks() # tjekker hvor længe projektilet har været "i live", så det kan blive fjernet efter

    def update (self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawnTime > PROJECTILE_LIFETIME: #Tjekker om spillerens projektil har været i live længere tid end vi ønsker
            self.kill() #Hvis sandt dræber vi vores projektil

