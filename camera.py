import pygame
from settings import *
import pytmx
from sprites import *

class TiledMap: 
    def __init__(self, filename):
        gameMap = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = gameMap.width * gameMap.tilewidth
        self.height = gameMap.height * gameMap.tileheight
        self.tmxdata = gameMap
    
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
             if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if(tile):
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    
    def objectlayer(self):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(Player.rect.x) == True:
                        print("Nice hit")
        
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
    
class Camera: 
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width 
        self.height = height 

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft) #Giver en ny rektangel der er shiftet

    def apply_rect(self, rect):
         return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0,x) #venstre
        y = min(0,y) # top
        x = max(-(self.width - WIDTH), x) #højre
        y = max(-(self.height - HEIGHT), y) #bund
        self.camera = pygame.Rect(x, y, self.width, self.height)