import io

import pygame as pg

from .engine import g
from .font import Font
from .group import Group
from .console import StreamConsole

from .sprites import BakedSprite, ReadlineSprite

class ReadlineScene(Group):

    def __init__(self):
        super().__init__()

        self.lines = []
        self.font = Font()

        self.readline = ReadlineSprite(">>> ")
        self.topleft = (g.screen.rect.left + 10, g.screen.rect.top + self.readline.rect.height + 10)
        self.readline.rect.topleft = self.topleft
        self.add(self.readline)

        self.console = StreamConsole(io.StringIO())

        g.engine.listen(pg.USEREVENT, self.on_userevent)

    def lastline(self):
        if self.lines:
            return self.lines[-1]
        else:
            return self.readline

    def on_userevent(self, event):
        if event.action != "readline":
            return

        image = self.font.render(self.readline.prompt + event.value)
        position = dict(topleft=self.readline.rect.topleft)
        self.add(BakedSprite(image, self, position=position))

        more = self.console.push(event.value)
        if more:
            self.readline.prompt = "... "
            self.readline.render()
        else:
            output = self.console.stream.getvalue()
            if output:
                image = self.font.render(self.readline.prompt + output)
                position = dict(topleft=self.readline.rect.bottomleft)
                self.add(BakedSprite(image, self, position=position))
                self.console.stream = io.StringIO()

            self.readline.prompt = ">>> "
            self.readline.render()

        last = self.sprites()[-1]
        self.readline.rect.topleft = last.rect.bottomleft
