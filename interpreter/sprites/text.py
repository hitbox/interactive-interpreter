import pygame as pg

from ..events import ReadlineEvent
from ..font import Font
from ..font import wrap
from ..globals import g

from .base import Sprite

class TextSprite(Sprite):

    def __init__(self, font, text, inside, *groups):
        super().__init__(*groups)
        self.font = font
        self.text = text
        self.rect = inside

        g.engine.listen(pg.KEYDOWN, self.on_keydown)

    def on_keydown(self, event):
        if event.key == pg.K_ESCAPE:
            g.engine.stop()

    @property
    def image(self):
        return self.font.render(self.text, self.rect)
