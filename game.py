import pygame 
import sys
from settings import*
from sprites import *

class Game:
    def __init__(self):
<<<<<<< HEAD
        pygame.init()
        self.screen = pygame.display.set_mode((500,500))
    
    def run(self): 
        # kører spillet = True, for at stoppe spil = False
        self.running = True 
        While self.running: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    running = False

 