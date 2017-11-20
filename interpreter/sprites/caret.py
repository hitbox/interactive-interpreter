import pygame as pg

from .base import Sprite

class SpriteCaret(Sprite):

    def __init__(self, size=(2,48)):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill((255,25,25))
        self.rect = self.image.get_rect()
