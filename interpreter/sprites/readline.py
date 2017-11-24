import pygame as pg

from ..engine import g, ReadlineEvent
from ..font import Font
from ..readline import Readline

from .base import Sprite
from .caret import CaretSprite

class ReadlineSprite(Sprite):

    def __init__(self, prompt, inside):
        super().__init__()

        self.font = Font()
        self.prompt = prompt

        size = self.font.size("X")
        self.rect = pg.Rect((0,0),size)

        self.active = True
        self.readline = Readline()

        self.caret = CaretSprite()
        self.inside = inside

        self.render()

    def on_keydown(self, event):
        if not self.active:
            return

        if event.key == pg.K_RETURN:
            value = self.readline.value
            g.engine.emit(ReadlineEvent(value))
            self.readline.clear()
        elif event.key == pg.K_ESCAPE:
            self.readline.clear()
        elif event.key == pg.K_BACKSPACE:
            self.readline.backspace()
        elif event.key == pg.K_UP:
            self.readline.history_up()
        elif event.key == pg.K_DOWN:
            self.readline.history_down()
        elif event.key == pg.K_LEFT:
            self.readline.move_left()
        elif event.key == pg.K_RIGHT:
            self.readline.move_right()
        else:
            self.readline.write(event.unicode)

        self.render()
        self.rect.size = self.image.get_size()

    def render(self):
        final = self.font.render(self.text, self.inside)
        self.image = final
        return final

    @property
    def text(self):
        "Return the full text, prompt + input"
        return self.prompt + self.readline.value

    def get_caret_rect(self):
        crects = [pg.Rect(self.rect.topleft,self.font.size(c)) for c in self.text]

        if len(crects) > 1:
            for cr1, cr2 in zip(crects[:-1], crects[1:]):
                cr2.bottomleft = cr1.bottomright

            pos = (len(self.prompt) - 1) + (self.readline.position)
            return crects[pos]

    def update(self):
        if self.text:
            self.caret.rect = self.get_caret_rect()
        self.render()

    def write(self, data):
        self.readline.write(data)
