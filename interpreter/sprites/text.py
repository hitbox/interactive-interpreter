import pygame as pg

from ..font import Font
from .base import Sprite

class Text(Sprite):

    def __init__(self, size, value=""):
        super().__init__()
        self.rect = pg.Rect((0,0),size)
        self.value = value
        self.font = Font()

    @property
    def image(self):
        return self.font.render(self.value)

    def write(self, data):
        self.value += data
