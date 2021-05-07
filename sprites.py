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
        self.last_shot = 0

    #Tjekker om brugeren vil bevæge sig med bevægelsestasterne, og om man kolliderer med træerne
    def get_keys(self):
        self.vel = vec (0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not self.game.hitDetectionLeftTrees(self.rect):
            self.vel.x = -PLAYER_SPEED 
        if keys[pygame.K_d] and not self.game.hitDetectionRightTrees(self.rect):
            self.vel.x = PLAYER_SPEED
        if keys[pygame.K_w] and not self.game.hitDetectionTopTrees(self.rect):
            self.vel.y = -PLAYER_SPEED
        if keys[pygame.K_s] and not self.game.hitDetectionBottomTrees(self.rect):
            self.vel.y = PLAYER_SPEED

        #Fikser bevægelsehastigheds inkonsistens
        if self.vel.x != 0 and self.vel.y != 0: # Tjekker om playeren bevæger sig i to retninger på samme tid, altså diagonalt
            self.vel *= 0.7071

         #Skudfunktion hvor man skyder ved kun at trykke på SPACE, protektilerne flyver i playerens retning   
        if keys[pygame.K_SPACE] and self.vel != (0,0):
            now = pygame.time.get_ticks()
            if now - self.last_shot > FIRERATE:
                self.last_shot = now
                dir = self.vel
                if self.vel.x < 0:
                    Projectile(self.game, self.pos + WAND_OFFSET, dir, "left")

                elif self.vel.x > 0:
                    Projectile(self.game, self.pos + WAND_OFFSET, dir, "right")

                elif self.vel.x == 0 and self.vel.y < 0:
                    Projectile(self.game, self.pos + WAND_OFFSET, dir, "up")

                elif self.vel.x == 0 and self.vel.y > 0:
                    Projectile(self.game, self.pos + WAND_OFFSET, dir, "down")
        
        #Skudfunktion hvor man bruger piltasterne for retning, giver mere brugervenlighed
        if keys[pygame.K_UP]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > FIRERATE:
                self.last_shot = now
                dir = vec(0,-PLAYER_SPEED)
                Projectile(self.game, self.pos + WAND_OFFSET, dir, "up")
        
        elif keys[pygame.K_DOWN]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > FIRERATE:
                self.last_shot = now
                dir = vec(0,PLAYER_SPEED)
                Projectile(self.game, self.pos + WAND_OFFSET, dir, "down")

        elif keys[pygame.K_RIGHT]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > FIRERATE:
                self.last_shot = now
                dir = vec(PLAYER_SPEED, 0)
                Projectile(self.game, self.pos + WAND_OFFSET, dir, "right")

        elif keys[pygame.K_LEFT]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > FIRERATE:
                self.last_shot = now
                dir = vec(-PLAYER_SPEED,0)
                Projectile(self.game, self.pos + WAND_OFFSET, dir, "left")
            

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

        if (self.game.hitDetectionTopTrees(self.rect) or self.game.hitDetectionLeftTrees(self.rect) 
        or self.game.hitDetectionRightTrees(self.rect) 
        or self.game.hitDetectionBottomTrees(self.rect)):
            self.vel = vec (0,0)
            
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2 #Equation of motion https://www.youtube.com/watch?v=SAbxZDBJX4E&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i&index=8&ab_channel=KidsCanCode
        self.rect.center = self.pos

class Projectile (pygame.sprite.Sprite):
    def __init__ (self, game, pos, dir, facing):
        self.groups = game.all_sprites, game.projectiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_not_rotated = pygame.image.load('PlayerProjectile.png')
        self.image = self.image_not_rotated
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(pos) #Laver en ny vector for vores projektil, ellers ville vi også update player pos
        self.rect.center = pos
        self.vel = dir * PROJECTILE_SPEED #Projektilet bruger en retningsvektor for at finde retningen den skal skydes i og ganger denne med farten
        self.spawnTime = pygame.time.get_ticks() # tjekker hvor længe projektilet har været "i live", så det kan blive fjernet efter
        self.facing = facing

    def update (self):
        if self.facing == "up":
            self.rotateProjectilePointingUp()
        if self.facing == "left":
            self.rotateProjectilePointingLeft()
        if self.facing == "down":
            self.rotateProjectilePointingDown()
            
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        if pygame.time.get_ticks() - self.spawnTime > PROJECTILE_LIFETIME: #Tjekker om spillerens projektil har været i live længere tid end vi ønsker
            self.kill() #Hvis sandt dræber vi projectile

        if (self.game.hitDetectionBottomTrees(self.rect) or self.game.hitDetectionLeftTrees(self.rect) 
        or self.game.hitDetectionRightTrees(self.rect) 
        or self.game.hitDetectionTopTrees(self.rect)):
            self.kill()


    def rotateProjectilePointingUp (self):
        self.image = pygame.transform.rotate(self.image_not_rotated, 90)

    def rotateProjectilePointingLeft (self):
        self.image = pygame.transform.rotate(self.image_not_rotated, 180)

    def rotateProjectilePointingDown (self):
        self.image = pygame.transform.rotate(self.image_not_rotated, 270)