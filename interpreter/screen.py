import pygame as pg

class Screen(object):

    def __init__(self, size):
        self.display = pg.display.set_mode(size)
        self.rect = self.display.get_rect()
        self.background = self.display.copy()
        self.background.fill((0,0,0))

    def clear(self):
        self.display.blit(self.background, (0,0))

    def flip(self):
        pg.display.flip()


def desktop_aligned(size, position, trim=8):
    """
    :param size: (width, height) of Screen.
    :param position: dict of rect attributes to align Rect((0,0), size) on.
                     e.g.: dict(midright="midright").
    :param trim: assume the window trim is this size.
    """
    from . import window

    desktop_rect = window.get_desktop_rect()
    display_rect = pg.Rect((0,0),size)
    display_rect.inflate_ip(trim, trim)

    for name, value in position.items():
        setattr(display_rect, name, getattr(desktop_rect, name))
    window.set_position(display_rect.topleft)

    return Screen(size)
