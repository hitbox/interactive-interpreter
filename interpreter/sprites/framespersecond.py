from functools import lru_cache

import pygame as pg

from ..globals import g
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
        return self.render("%.2f" % self._fps)

    @lru_cache(None)
    def render(self, text):
        return self.font.render(text)

    def update(self):
        self._fps = g.clock.get_fps()
