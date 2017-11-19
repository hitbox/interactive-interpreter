import pygame as pg

from . import join

class Font(object):

    def __init__(self, size=32, color=(255,255,255)):
        self._font = pg.font.Font(None, size)
        self.color = color
        self.antialias = True
        self.empty = pg.Surface((0,0))

    def render(self, text):
        if not text:
            return self.empty
        lines = text.splitlines()
        images = [self._font.render(line, self.antialias, self.color)
                  for line in lines]
        return join.top2bottom(images)

    def size(self, text):
        if not text:
            return (0, 0)
        lines = text.splitlines()
        sizes = [self._font.size(line) for line in lines]
        width = max(size[0] for size in sizes)
        height = sum(size[1] for size in sizes)
        return (width, height)
