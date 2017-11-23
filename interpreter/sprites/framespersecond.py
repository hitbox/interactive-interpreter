import pygame as pg

from ..engine import g
from ..font import Font

from .base import Sprite

class FramesPerSecondSprite(Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)
        self.font = Font()
        self.rect = pg.Rect((0,0),self.font.size("     "))
        self._fps = 999.99

    @property
    def image(self):
        return self.font.render("%.2f" % self._fps)

    def update(self):
        self._fps = g.clock.get_fps()
