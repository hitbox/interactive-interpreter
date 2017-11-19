import pygame as pg

from ..engine import g
from ..console import Console
from .base import Sprite
from .textbox import SpriteTextbox
from .text import Text

class SpriteConsole(Sprite):

    # XXX: subclass this as Sprite, InteractiveInterpreter all the way down?

    def __init__(self, locals=None):
        super().__init__()

        size = (g.screen.rect.width - 10, g.screen.rect.height / 4)
        self.spritetextbox = SpriteTextbox(size)
        self.spritetextbox.position = dict(midbottom=(g.screen.rect.centerx, g.screen.rect.bottom - 10))

        self.console = Console(self.spritetextbox, locals=locals)

        self.stderr = Text()

    @property
    def image(self):
        return self.spritetextbox.image

    @property
    def rect(self):
        return self.spritetextbox.rect

    def on_keydown(self, event):
        self.console.on_keydown(event)

    def update(self):
        self.spritetextbox.update()
