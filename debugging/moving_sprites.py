import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame as pg

from interpreter import screen
from interpreter.engine import Engine
from interpreter.globals import g
from interpreter.scenes import BaseScene
from interpreter.sprites import Sprite
from interpreter.tween import Tween

class MovingSprite(Sprite):

    def moveto(self, target, steps):
        self.xt = Tween(self.rect.x, target.x, steps)
        self.yt = Tween(self.rect.y, target.y, steps)

    def update(self):
        if hasattr(self, "xt"):
            try:
                x = next(self.xt)
                self.rect.x = x
            except StopIteration:
                del self.xt

        if hasattr(self, "yt"):
            try:
                y = next(self.yt)
                self.rect.y = y
            except StopIteration:
                del self.yt

class MovingSpriteScene(BaseScene):

    def __init__(self):
        super().__init__()

        sprite = MovingSprite()
        sprite.image = pg.Surface((100, 50))
        sprite.image.fill((200,100,100))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = g.screen.rect.center
        self.add(sprite)

        target = sprite.rect.copy()
        target.midright = g.screen.rect.midright
        sprite.moveto(target, 60*3)

        g.engine.listen(pg.KEYDOWN, self.on_keydown)

    def on_keydown(self, event):
        if event.key in (pg.K_q, pg.K_ESCAPE):
            g.engine.stop()


def main():
    engine = Engine(screen.desktop_aligned((1000,900), dict(midright="midright")))
    engine.run(MovingSpriteScene())

if __name__ == "__main__":
    main()
