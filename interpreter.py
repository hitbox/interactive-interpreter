import code
import os

import pygame as pg

pg.display.init()
pg.font.init()

SCREEN_SIZE = (640, 480)

# position window like midright, leaving room on the left to see logging.
info = pg.display.Info()
x = (info.current_w - SCREEN_SIZE[0]) - 10
y = (info.current_h - SCREEN_SIZE[1]) / 2

os.environ['SDL_VIDEO_WINDOW_POS'] = '%s,%s' % (x, y)

del info, x, y

FONT_SIZE = 32

def join(images):
    rects = [image.get_rect() for image in images]

    final_rect = pg.Rect(0, 0, max(rect.width for rect in rects), sum(rect.height for rect in rects))
    final_image = pg.Surface(final_rect.size, pg.SRCALPHA)

    y = 0
    for rect, image in zip(rects, images):
        final_image.blit(image, (0, y))
        y += rect.height

    return final_image

class draw:

    @staticmethod
    def border(image, color=(255,255,255), thickness=1):
        pg.draw.rect(image, color, image.get_rect(), thickness)
        return image

class g:

    engine = None
    screen = None


class Clock(object):

    def __init__(self, framerate=60):
        self._clock = pg.time.Clock()
        self.framerate = framerate

    def tick(self):
        return self._clock.tick(self.framerate)


class Screen(object):

    def __init__(self, SCREEN_SIZE):
        self.display = pg.display.set_mode(SCREEN_SIZE)
        self.rect = self.display.get_rect()

    def clear(self):
        self.display.fill((0,0,0))

    def flip(self):
        pg.display.flip()


class Caret(object):

    def __init__(self):
        pass


class Input(object):

    def __init__(self):
        pass


class Textbox(Input):

    def __init__(self):
        self.value = ''

    def on_keydown(self, event):
        if event.key == pg.K_BACKSPACE:
            chars = list(self.value)
            try:
                chars.pop()
            except IndexError:
                pass
            else:
                self.value = ''.join(chars)
        else:
            self.value += event.unicode


class Font(object):

    def __init__(self, size=FONT_SIZE, color=(255,255,255)):
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
        return join(images)

    def size(self, text):
        if not text:
            return (0, 0)
        lines = text.splitlines()
        sizes = [self._font.size(line) for line in lines]
        width = max(size[0] for size in sizes)
        height = sum(size[1] for size in sizes)
        return (width, height)


class Group(pg.sprite.Group):
    pass


class Sprite(pg.sprite.Sprite):
    pass


class SpriteTextbox(Sprite):

    def __init__(self, size, position=None):
        super().__init__()
        self.textbox = Textbox()
        self.rect = pg.Rect((0,0),(size))
        self.font = Font()
        self.position = position

    @property
    def image(self):
        textimage = self.font.render(self.textbox.value)
        textrect = textimage.get_rect()

        rect = self.rect.copy()
        if rect.height < textrect.height:
            rect.height = textrect.height

        final = pg.Surface(rect.size, pg.SRCALPHA)

        position = textimage.get_rect(bottomleft=final.get_rect().bottomleft)
        final.blit(textimage, position)

        draw.border(final)
        return final

    @property
    def value(self):
        return self.textbox.value

    def on_keydown(self, event):
        self.textbox.on_keydown(event)

    def update(self):
        if self.position:
            for key, value in self.position.items():
                setattr(self.rect, key, value)


class Console(code.InteractiveInterpreter):

    def __init__(self, spritetextbox, locals=None, filename='<console>'):
        super().__init__(locals)
        self.spritetextbox = spritetextbox
        self.filename = filename
        self.resetbuffer()

    def on_keydown(self, event):
        self.spritetextbox.on_keydown(event)
        if event.key == pg.K_RETURN:
            self.runsource(self.spritetextbox.value)
            line = self.spritetextbox.textbox.value
            self.spritetextbox.textbox.value = ''
            more = self.push(line)

    def push(self, line):
        self.buffer.append(line)
        source = '\n'.join(self.buffer)
        more = self.runsource(source, self.filename)
        if not more:
            self.resetbuffer()
        return more

    def resetbuffer(self):
        self.buffer = []

    def write(self, data):
        self.spritetextbox.textbox.value += data


class SpriteConsole(Sprite):

    def __init__(self, locals=None):
        super().__init__()

        size = (g.screen.rect.width - 10, g.screen.rect.height / 4)
        self.spritetextbox = SpriteTextbox(size)
        self.spritetextbox.position = dict(midbottom=(g.screen.rect.centerx, g.screen.rect.bottom - 10))

        self.console = Console(self.spritetextbox, locals=locals)

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


class ConsoleScene(Group):

    def __init__(self, locals=None):
        super().__init__()

        self.console = SpriteConsole(locals)
        self.add(self.console)


class Engine(object):

    def __init__(self):
        g.engine = self
        self.clock = Clock()
        g.screen = self.screen = Screen(SCREEN_SIZE)

        self.scene = ConsoleScene(globals())

        self.is_running = False

        pg.key.set_repeat(150, 50)

    def run(self):
        self.is_running = True
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False
                elif event.type == pg.KEYDOWN:
                    # TODO: handle keydown that quits better
                    if event.key in (pg.K_q, pg.K_ESCAPE):
                        pg.event.post(pg.event.Event(pg.QUIT))
                    else:
                        for sprite in self.scene.sprites():
                            if hasattr(sprite, 'on_keydown'):
                                sprite.on_keydown(event)

            self.scene.update()

            self.screen.clear()
            self.scene.draw(self.screen.display)
            self.screen.flip()


def main():
    engine = Engine()
    engine.run()

if __name__ == '__main__':
    main()
