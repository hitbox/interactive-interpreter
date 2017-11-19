import pygame as pg

from .base import Sprite
from .. import draw
from ..font import Font
from ..textbox import Textbox

class SpriteTextbox(Sprite):

    def __init__(self, size, position=None):
        super().__init__()
        self.textbox = Textbox()
        self.rect = pg.Rect((0,0),(size))
        self.font = Font()
        self.position = position

    @property
    def image(self):
        textimage = self.font.render(self.textbox.value)
        textrect = textimage.get_rect()

        rect = self.rect.copy()
        if rect.height < textrect.height:
            rect.height = textrect.height

        final = pg.Surface(rect.size, pg.SRCALPHA)

        position = textimage.get_rect(bottomleft=final.get_rect().bottomleft)
        final.blit(textimage, position)

        draw.border(final)
        return final

    @property
    def value(self):
        return self.textbox.value

    def on_keydown(self, event):
        self.textbox.on_keydown(event)

    def update(self):
        if self.position:
            for key, value in self.position.items():
                setattr(self.rect, key, value)
