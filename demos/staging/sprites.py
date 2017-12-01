from collections import deque

import pygame as pg

from interpreter.sprites import Sprite
from interpreter.tween import Tween

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

    def movetos(self, targets, steps):
        for target in targets:
            self.moveto(target, steps)

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


class Crosshair(Sprite):

    def __init__(self, size):
        super().__init__()
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect()
        color = (255,0,0)
        pg.draw.line(self.image, color, self.rect.midtop, self.rect.midbottom)
        pg.draw.line(self.image, color, self.rect.midleft, self.rect.midright)
        radius = int(min((self.rect.width, self.rect.height)) / 2)
        pg.draw.circle(self.image, color, self.rect.center, radius, 1)
        radius = int(min((self.rect.width, self.rect.height)) / 4)
        pg.draw.circle(self.image, color, self.rect.center, radius, 1)


def huestrip(size):
    if isinstance(size, pg.Rect):
        size = size.size
    surface = pg.Surface(size)
    width, height = size

    for x in range(width):
        hue = int(360 * (x / width))
        color = pg.Color(0)
        color.hsva = hue, 100, 100, 100
        pg.draw.line(surface, color, (x, 0), (x, height))

    return surface

def saturationvalue(surface, hue):
    width, height = surface.get_size()

    for x in range(width):
        saturation = int(100 * (x / width))
        for y in range(height):
            value = int(100 * (y / height))
            color = pg.Color(0)
            color.hsva = (hue, saturation, value, 100)
            surface.set_at((x, height - y - 1), color)
            yield

def colorsquare(size):
    if isinstance(size, pg.Rect):
        size = size.size
    surface = pg.Surface(size)
    width, height = size

    for x in range(width):
        for y in range(height):
            color = tuple(map(int, (255*(x/width), 255*(y/height), 255)))
            surface.set_at((x, y), color)

    return surface
