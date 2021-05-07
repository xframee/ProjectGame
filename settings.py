import pygame
vec = pygame.math.Vector2
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (35, 35, 35)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1400   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 700  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
GAME_TITLE = "Super fedt spil"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# player attributes
PLAYER_SPEED = 300
WAND_OFFSET = vec(20,5)

# Weapon attributes
PROJECTILE_SPEED = 1.5 #Hastigheden på vores projektil i forhold til hastigheden på vores player
PROJECTILE_LIFETIME = 5000
FIRERATE = 500 #Tid i millisekunder mellem hvert skud

# Enemy attributes
MOB_SPEED = 200