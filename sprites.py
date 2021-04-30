import pygame
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.game = game
        self.image = pygame.image.load('player1.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x 
        self.rect.y = self.y

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