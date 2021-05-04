import pygame
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.vx, self.vy = 0, 0
        self.game = game
        self.image = pygame.image.load('player1.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not self.game.hitDetectionLeftTrees():
            self.vx = -PLAYER_SPEED 
        elif keys[pygame.K_d] and not self.game.hitDetectionRightTrees():
            self.vx = PLAYER_SPEED
        elif keys[pygame.K_w] and not self.game.hitDetectionTopTrees():
            self.vy = -PLAYER_SPEED
        elif keys[pygame.K_s] and not self.game.hitDetectionBottomTrees():
            self.vy = PLAYER_SPEED

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.topleft = (self.x, self.y)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.game = game
        self.image = pygame.image.load('enemy1.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y