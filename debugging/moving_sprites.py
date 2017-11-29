import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from collections import deque

import pygame as pg

from interpreter import screens
from interpreter.engine import Engine
from interpreter.globals import g
from interpreter.scenes import BaseScene
from interpreter.scenes import ReadlineScene
from interpreter.sprites import Sprite, FramesPerSecondSprite
from interpreter.tween import Tween
from interpreter.utils import positioned

class MovingSprite(Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)
        self.paths = deque()

    def moveto(self, target, steps):
        lastx, lasty = None, None

        if self.paths:
            lastxtween, lastytween = self.paths[0]
            lastx, lasty = map(int, (lastxtween.end, lastytween.end))
        else:
            xtween = getattr(self, "xtween", None)
            ytween = getattr(self, "ytween", None)
            if xtween:
                lastx = int(xtween.end)
            else:
                lastx = self.rect.x
            if ytween:
                lasty = int(ytween.end)
            else:
                lasty = self.rect.y

        xtween = Tween(lastx, target.x, steps)
        ytween = Tween(lasty, target.y, steps)
        self.paths.appendleft((xtween, ytween))

    def update_moveto(self):
        hasxtween, hasytween = hasattr(self, "xtween"), hasattr(self, "ytween")
        if hasxtween:
            try:
                self.rect.x = next(self.xtween)
            except StopIteration:
                self.rect.x = self.xtween.end
                del self.xtween

        if hasytween:
            try:
                self.rect.y = next(self.ytween)
            except StopIteration:
                self.rect.y = self.ytween.end
                del self.ytween

        if not hasxtween and not hasytween and self.paths:
            self.xtween, self.ytween = self.paths.pop()

    def update(self):
        self.update_moveto()


class MovingSpriteScene(BaseScene):

    def __init__(self):
        super().__init__()

        leftside = g.screen.rect.copy()
        leftside.width /= 2

        rightside = g.screen.rect.copy()
        rightside.width /= 2
        rightside.topright = g.screen.rect.topright

        pg.draw.rect(g.screen.background,(90,90,90),leftside,1)
        pg.draw.rect(g.screen.background,(90,90,90),rightside,1)

        sprite = MovingSprite()
        sprite.image = pg.Surface((100, 50))
        sprite.image.fill((200,100,100))
        sprite.rect = sprite.image.get_rect()
        self.add(sprite)

        fps = FramesPerSecondSprite()
        fps.rect.topright = leftside.topright
        self.add(fps)

        steps = 60

        context = dict(g=g, pg=pg, sprite=sprite, s=sprite, positioned=positioned,
                       leftside=leftside, rightside=rightside, steps=steps)

        self.subscene = ReadlineScene(leftside.inflate(-100, -100), context)
        pg.draw.rect(g.screen.background,(90,200,90),self.subscene.inside,1)

        sprite.rect.center = rightside.center
        sprite.moveto(positioned(sprite.rect, midright=rightside.midright), steps)
        sprite.moveto(positioned(sprite.rect, topright=rightside.topright), steps)
        sprite.moveto(positioned(sprite.rect, topleft=rightside.topleft), steps)
        sprite.moveto(positioned(sprite.rect, bottomleft=rightside.bottomleft), steps)
        sprite.moveto(positioned(sprite.rect, bottomright=rightside.bottomright), steps)
        sprite.moveto(positioned(sprite.rect, center=rightside.center), steps)

        save = self.subscene.readlinesprite.readline.history.add

        save("steps = 60")
        save("sprite.rect.center = rightside.center")
        save("sprite.moveto(positioned(sprite.rect, midright=rightside.midright), steps)")
        save("sprite.moveto(positioned(sprite.rect, topright=rightside.topright), steps)")
        save("sprite.moveto(positioned(sprite.rect, topleft=rightside.topleft), steps)")
        save("sprite.moveto(positioned(sprite.rect, bottomleft=rightside.bottomleft), steps)")
        save("sprite.moveto(positioned(sprite.rect, bottomright=rightside.bottomright), steps)")
        save("sprite.moveto(positioned(sprite.rect, center=rightside.center), steps)")

    def draw(self, surface):
        super().draw(surface)
        self.subscene.draw(surface)

    def update(self):
        super().update()
        self.subscene.update()


def main():
    screen = screens.desktop_aligned_center((1800,600))
    engine = Engine(screen)
    engine.run(MovingSpriteScene())

if __name__ == "__main__":
    main()
