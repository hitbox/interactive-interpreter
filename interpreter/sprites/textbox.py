import pygame as pg

from .. import draw
from ..font import Font
from ..textbox import Textbox

from .base import Sprite
from .caret import SpriteCaret

class SpriteTextbox(Sprite):

    def __init__(self, size, value="", position=None):
        super().__init__()
        self.textbox = Textbox()
        self.rect = pg.Rect((0,0),(size))
        self.font = Font()
        self.position = position
        self.caret = SpriteCaret(self.font.size("|"))

    @property
    def image(self):
        textimage = self.font.render(self.textbox.value)
        textrect = textimage.get_rect()

        rects = []
        x, y = 0, textrect.top
        for index, char in enumerate(self.textbox.value):
            if index > self.textbox.position:
                # we only need to get rects up to the caret position
                break

            w, h = self.font.size(char)
            if char == "\n":
                x = 0
                y += h
                continue
            rect = pg.Rect(x, y, w, h)
            rects.append(rect)
            x += w
        if rects:
            caret_rect = rects[self.textbox.position-1]
            textimage.blit(self.caret.image, caret_rect)

        rect = self.rect.copy()
        if rect.height < textrect.height:
            rect.height = textrect.height

        final = pg.Surface(rect.size, pg.SRCALPHA)

        #position = textimage.get_rect(bottomleft=final.get_rect().bottomleft)
        #final.blit(textimage, position)
        final.blit(textimage, (0,0))

        return final

    @property
    def value(self):
        return self.textbox.value

    @value.setter
    def value(self, value):
        self.textbox.value = value

    def on_keydown(self, event):
        if event.key == pg.K_BACKSPACE:
            self.textbox.backspace()
        else:
            self.textbox.write(event.unicode)

    def update(self):
        self.rect = self.image.get_rect()
        if self.position:
            for key, value in self.position.items():
                setattr(self.rect, key, value)
