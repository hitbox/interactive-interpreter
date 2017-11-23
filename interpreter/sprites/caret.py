import pygame as pg

from .. import draw
from ..engine import g
from ..font import Font

from .base import Sprite

class CaretSprite(Sprite):

    def __init__(self):
        super().__init__()
        self.elapsed = 0
        self.timer = 500
        self.show = True

        self.font = Font()
        size = self.font.size(" ")

        self.images = {False: pg.Surface(size, pg.SRCALPHA),
                       True: pg.Surface(size, pg.SRCALPHA)}

        show_image = self.images[True]
        draw.borderright(show_image, self.font.color, 2)

        self.image = self.images[self.show]
        self.rect = self.image.get_rect()

    def update(self):
        self.elapsed += g.elapsed
        if self.elapsed > self.timer:
            self.elapsed %= self.timer
            self.show = not self.show
            self.image = self.images[self.show]
