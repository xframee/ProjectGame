import pygame
from settings import *

class Camera: 
    def __init__(self, width, height):
        self.camera = pygame.Rect(10, 10, width, height)
        self.width = width 
        self.height = height 

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft) #Giver en ny rektangel der er shiftet

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)
