import pygame as pg

from ..events import ReadlineEvent
from ..font import Font
from ..font import wrap
from ..globals import g
from ..readline import Readline

from .base import Sprite
from .caret import CaretSprite

class ReadlineSprite(Sprite):
    """
    """
    def __init__(self, prompt, inside, *groups):
        super().__init__(*groups)

        self.font = Font()
        self.prompt = prompt

        size = self.font.size("X")

        self.active = True
        self.readline = Readline()

        self.inside = inside
        self.rect = self.inside

        self.caret = CaretSprite()

        self.render()

        g.engine.listen(pg.KEYDOWN, self.on_keydown)

    def get_caret_rect(self):
        crects = wrap(self.font, self.inside, self.text)
        pos = (len(self.prompt) - 1) + self.readline.position
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
        # history up/down
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
        elif event.key == pg.K_HOME:
            self.readline.move_start()
        elif event.key == pg.K_END:
            self.readline.move_end()
        # send string through
        else:
            self.write(event.unicode)

        self.render()
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
