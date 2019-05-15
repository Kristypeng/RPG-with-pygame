###
# This TiledMap import method is cited from Chris Bradfield
###

import pygame
import pytmx
from settings import *
vec = pygame.math.Vector2

class Tiledmap(object):
    def __init__ (self, filename):
        self.loadmap = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = self.loadmap.width * self.loadmap.tilewidth
        self.height = self.loadmap.height * self.loadmap.tileheight

    def build(self, surface):
        maptile = self.loadmap.get_tile_image_by_gid
        for layer in self.loadmap.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = maptile(gid)
                    if tile:
                        surface.blit(tile, (x * self.loadmap.tilewidth,
                                            y * self.loadmap.tileheight))

    def makeMap(self):
        mapsurface = pygame.Surface((self.width, self.height))
        self.build(mapsurface)
        return mapsurface


class Scrollwindow(object):
    def __init__(self, width, height):
        self.window = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.window.topleft)

    def apply_rect(self, rect):
        return rect.move(self.window.topleft)

    def update(self, target):
        x = -target.rect.x + int(screenW/2)
        y = -target.rect.y + int(screenH/2)
        self.window = pygame.Rect(x, y, self.width, self.height)
