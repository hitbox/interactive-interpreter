import pygame as pg

from . import join

class Wrapper:

    def __init__(self):
        self._cache = {}

    def _wrapper(self, font, inside, text):
        char_rects = []
        last = None
        for char in text:
            rect = pg.Rect((0,0),font.size(char))
            if last is None:
                rect.topleft = inside.topleft
            else:
                rect.bottomleft = last.bottomright
                if rect.right > inside.right:
                    rect.topleft = (inside.left, last.bottom)
            last = rect
            if char == "\n":
                rect.topleft = (inside.left, last.bottom)
            if rect.bottom > inside.bottom:
                break
            char_rects.append(rect)
        return char_rects

    def __call__(self, font, inside, text):
        key = (font, tuple(inside), text)
        if key not in self._cache:
            self._cache[key] = self._wrapper(font, inside, text)
        return self._cache[key]


class Font:

    def __init__(self, fontsize=20, color=(255,255,255), name=None):
        self._fonts = {}
        if name is None:
            name = "Consolas, DejaVu Sans Mono, Courier New"
        self.name = name
        self.fontsize = fontsize
        self.color = color
        self.antialias = True
        self.empty = pg.Surface((0,0))

        self._cache = {}
        self.wrapper = Wrapper()

    def __hash__(self):
        return id(self) + id(self._get_font())

    def _get_font(self):
        key = (self.name, self.fontsize)
        if key not in self._fonts:
            self._fonts[key] = pg.font.SysFont(self.name, self.fontsize)
        return self._fonts[key]

    def _render_inside(self, font, text, inside):
        rects = self.wrapper(font, inside, text)

        minleft = min(rect.left for rect in rects)
        mintop = min(rect.top for rect in rects)
        maxright = max(rect.right for rect in rects)
        maxbottom = max(rect.bottom for rect in rects)

        size = (maxright - minleft), (maxbottom - mintop)
        final = pg.Surface(size, pg.SRCALPHA)

        x, y = map(lambda v: -v, inside.topleft)
        for char, rect in zip(text, rects):
            if char == "\n":
                continue
            image = font.render(char, self.antialias, self.color)
            final.blit(image, rect.move(x, y))
        return final

    def _render_top2bottom(self, font, text):
        lines = text.splitlines()
        images = [font.render(line, self.antialias, self.color) for line in lines]
        final = join.top2bottom(images)
        return final

    def render(self, text, inside=None):
        font = self._get_font()
        if inside is None:
            key = (text, inside, font)
        else:
            key = (text, tuple(inside), font)
        if key not in self._cache:
            if not text:
                final = self.empty
            else:
                if inside:
                    final = self._render_inside(font, text, inside)
                else:
                    final = self._render_top2bottom(font, text)
            self._cache[key] = final
        return self._cache[key]

    def size(self, text):
        if not text:
            return (0, 0)
        font = self._get_font()
        lines = text.splitlines()
        sizes = [font.size(line) for line in lines]
        width = max(size[0] for size in sizes)
        height = sum(size[1] for size in sizes)
        return (width, height)
