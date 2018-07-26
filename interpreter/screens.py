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


def desktop_aligned(size, position, trim=None):
    """
    Set the environment variable that will align the pygame.display, and return
    a Screen object.

    :param size: (width, height) of Screen.
    :param position: dict of rect attributes to align Rect((0,0), size) on.
                     e.g.: dict(midright="midright").
    :param trim: assume the window trim is this size. default: 8.
    """
    from . import window

    if trim is None:
        trim = 8

    desktop_rect = window.get_desktop_rect()
    display_rect = pg.Rect((0,0),size)
    display_rect.inflate_ip(trim, trim)

    for name, value in position.items():
        setattr(display_rect, name, getattr(desktop_rect, name))
    window.set_position(display_rect.topleft)

    return Screen(size)

def desktop_aligned_midright(size, trim=None):
    """
    Return a Screen object aligned to the middle-right.
    """
    # mainly keeping this here to remember how to use `desktop_aligned`
    position = dict(midright="midright")
    return desktop_aligned(size, position=position, trim=trim)

def desktop_aligned_center(size, trim=None):
    """
    Return a Screen object aligned to the center.
    """
    position = dict(center="center")
    return desktop_aligned(size, position=position, trim=trim)
