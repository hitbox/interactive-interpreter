import io

import pygame as pg

from .engine import g
from .font import Font
from .group import Group
from .console import StreamConsole

from .sprites import ReadlineSprite, Sprite, SpriteConsole

class ConsoleScene(Group):

    def __init__(self, locals=None):
        super().__init__()

        self.console = SpriteConsole(locals)
        self.add(self.console)


class BakedSprite(Sprite):

    def __init__(self, image, *groups, position=None):
        super().__init__(*groups)
        self.image = image
        if position is None:
            position = {}
        self.rect = self.image.get_rect(**position)


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

        # XXX: almost there! it seems to be putting extra space between lines
        image = self.font.render(self.readline.prompt + event.value)
        position = dict(topleft=self.readline.rect.topleft)
        self.add(BakedSprite(image, self, position=position))

        more = self.console.push(event.value)
        if more:
            self.readline.prompt = "... "
            self.readline.render()
        else:
            output = self.console.stream.getvalue()
            print(('output', output))
            if output:
                image = self.font.render(self.readline.prompt + output)
                position = dict(topleft=self.readline.rect.bottomleft)
                self.add(BakedSprite(image, self, position=position))
                self.console.stream = io.StringIO()

            self.readline.prompt = ">>> "
            self.readline.render()

        self.readline.rect.topleft = self.readline.rect.bottomleft
        self.readline.rect.topleft = self.readline.rect.bottomleft

        if False and len(self.lines) > 1:
            print((self, self.lines))
            first = self.lines[0]
            first.rect.topleft = self.topleft
            for line1, line2 in zip(self.lines[:-1], self.lines[1:]):
                line2.rect.topleft = line1.rect.bottomleft

            #self.readline.rect.topleft = line2.rect.bottomleft
