import io

import pygame as pg

from .. import draw
from ..console import StreamConsole
from ..engine import g
from ..join import top2bottom

from .base import Sprite
from .textbox import SpriteTextbox

class SpriteConsole(Sprite):

    def __init__(self, locals=None):
        super().__init__()

        size = (g.screen.rect.width - 10, g.screen.rect.height / 4)
        self.spritetextbox = SpriteTextbox(size)
        self.spritetextbox.position = dict(midbottom=(g.screen.rect.centerx, g.screen.rect.bottom - 10))

        self.resetconsole()

    def resetconsole(self):
        self.console = StreamConsole(io.StringIO(), locals=locals())

    @property
    def image(self):
        return draw.border(self.spritetextbox.image)

    @property
    def rect(self):
        return self.spritetextbox.rect

    def on_keydown(self, event):
        self.spritetextbox.on_keydown(event)
        if event.key == pg.K_RETURN:
            more = self.console.push(self.spritetextbox.textbox.last_line())
            if not more:
                # XXX: how to make this behave like std{err,out}?
                self.spritetextbox.textbox.write(self.console.stream.getvalue() + "\n")
                self.resetconsole()
                return
        print(self.console.buffer)

    def update(self):
        self.spritetextbox.update()
