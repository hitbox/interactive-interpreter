import pygame as pg

from .sprites import Sprite

class Group(pg.sprite.Group):

    def add(self, *sprites):
        # add direct attributes of sprites that are also sprites
        more = []
        for sprite in sprites:
            for name in dir(sprite):
                obj = getattr(sprite, name)
                if isinstance(obj, Sprite):
                    more.append(obj)
        super().add(*sprites, *more)
