import pygame as pg

from . import join, Rect

# Left off here, thinking about word-wrapping.

def wrap(font, inside, text):
    """
    Wrap `text` that would be rendered with `font` inside the `inside`
    rect, returning where the character rects would be.

    :param font: a Pygame font.
    :type font: pygame.Font

    :param inside: a Rect, to wrap the rendered text inside of.
    :type inside: pygame.Rect, interpreter.rect.Rect

    :param text: the text to render with `font`.
    :type text: str
    """
    char_rects = []
    last = None
    for char in text:
        rect = Rect(font.size(char))
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

class Font:
    """
    Like pygame.Font, supporting newline characters. Also supports keeping
    attributes of the font in the instance, instead of passing them as
    arguments.
    """
    # pygame.Font is actually a function so it can't be subclassed

    def __init__(
            self,
            fontsize = 20,
            color = (255,255,255),
            name = None
        ):
        """
        :param fontsize: size of the font.
        :type fontsize: int

        :param color: color of the font.
        :type color: tuple, pygame.Color

        :param name: optional system name of font.
        :type name: None, str
        """
        if name is None:
            name = "Consolas, DejaVu Sans Mono, Courier New"
        self.name = name
        self.fontsize = fontsize
        self.color = color
        self.antialias = True
        self.empty = pg.Surface((0,0))

        self._font = pg.font.SysFont(self.name, self.fontsize)
        self._cache = {}

    def __hash__(self):
        return id(self) + id(self._font)

    def _render_inside(self, font, text, inside):
        rects = wrap(font, inside, text)

        minleft = min(rect.left for rect in rects)
        mintop = min(rect.top for rect in rects)
        maxright = max(rect.right for rect in rects)
        maxbottom = max(rect.bottom for rect in rects)

        size = (maxright - minleft), (maxbottom - mintop)
        final = pg.Surface(size, pg.SRCALPHA)

        offset = tuple(map(lambda v: -v, inside.topleft))
        for char, rect in zip(text, rects):
            if char == "\n":
                continue
            image = font.render(char, self.antialias, self.color)
            final.blit(image, rect.move(*offset))
        return final

    def _render_top2bottom(self, font, text):
        lines = text.splitlines()
        images = [font.render(line, self.antialias, self.color) for line in lines]
        final = join.top2bottom(images)
        return final

    def render(self, text, inside=None):
        """
        Render `text`, optionally wrapped inside a rect, returning the rendered image.

        :param text: the text to render.
        :type text: str

        :param inside: optional rect to wrap `text` inside of.
        :type inside: pygame.Rect
        """
        if inside is None:
            key = (text, inside, self._font)
        else:
            key = (text, tuple(inside), self._font)
        if key not in self._cache:
            if not text:
                final = self.empty
            else:
                if inside:
                    final = self._render_inside(self._font, text, inside)
                else:
                    final = self._render_top2bottom(self._font, text)
            self._cache[key] = final
        return self._cache[key]

    def size(self, text):
        """
        Like pygame.Font.size, supporting interpretation of newline characters
        as actual lines.

        :param text: text to get the size of.
        :type text: str
        """
        if not text:
            return (0, 0)
        lines = text.splitlines()
        line_sizes = [self._font.size(line) for line in lines]
        width = max(size[0] for size in line_sizes)
        height = sum(size[1] for size in line_sizes)
        return (width, height)
