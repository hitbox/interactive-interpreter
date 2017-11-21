import pygame as pg

from ..engine import g, ReadlineEvent
from ..font import Font
from ..textbox import Textbox

from .base import Sprite

class ReadlineSprite(Sprite):

    def __init__(self, prompt):
        super().__init__()

        self.font = Font()
        self.prompt = prompt

        size = self.font.size("X")
        self.rect = pg.Rect((0,0),size)

        self.active = True
        self.textbox = Textbox()

        self.render()

    def on_keydown(self, event):
        if not self.active:
            return

        if event.key == pg.K_RETURN:
            g.engine.emit(ReadlineEvent(self.textbox.value))
            self.textbox.clear()
        elif event.key == pg.K_BACKSPACE:
            self.textbox.backspace()
        else:
            self.textbox.write(event.unicode)

        self.render()
        self.rect.size = self.image.get_size()

    def render(self):
        image = self.font.render(self.prompt + self.textbox.value)
        self.image = image
        return image
