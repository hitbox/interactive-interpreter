import pygame as pg

from ..events import ReadlineEvent
from ..font import Font
from ..globals import g
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

    def get_caret_rect(self):
        crects = [pg.Rect(self.rect.topleft,self.font.size(c)) for c in self.text]

        if len(crects) > 1:
            for cr1, cr2 in zip(crects[:-1], crects[1:]):
                cr2.bottomleft = cr1.bottomright

            pos = (len(self.prompt) - 1) + (self.readline.position)
            return crects[pos]

    def on_keydown(self, event):
        if not self.active:
            return
        rv = None
        # submit
        if event.key == pg.K_RETURN:
            rv = self.submit()
        # clear
        elif event.key == pg.K_ESCAPE:
            self.readline.clear()
        # backspace
        elif event.key == pg.K_BACKSPACE:
            self.readline.backspace()
        # delete
        elif event.key == pg.K_DELETE:
            self.readline.delete()
        # history
        elif event.key == pg.K_UP:
            rv = self.readline.history_up()
        elif event.key == pg.K_DOWN:
            rv = self.readline.history_down()
        # CTRL+D
        elif event.key == pg.K_d and event.mod & pg.KMOD_CTRL:
            g.engine.stop()
        # move caret
        elif event.key == pg.K_LEFT:
            self.readline.move_left()
        elif event.key == pg.K_RIGHT:
            self.readline.move_right()
        # send string through
        else:
            self.write(event.unicode)

        self.render()
        self.rect.size = self.image.get_size()
        return rv

    def render(self):
        final = self.font.render(self.text, self.inside)
        self.image = final
        return final

    def submit(self):
        value = self.readline.submit()
        g.engine.emit(ReadlineEvent("submit", value))
        return value

    @property
    def text(self):
        "Return the full text, prompt + input"
        return self.prompt + self.readline.value

    def update(self):
        if self.text:
            self.caret.rect = self.get_caret_rect()
        self.render()

    def write(self, data):
        self.readline.write(data)
        g.engine.emit(ReadlineEvent("write", data))
