import os

import pygame as pg

def get_desktop_rect():
    """
    Return the desktop size as Rect. Call before `pygame.display.set_mode`.
    """
    info = pg.display.Info()
    return pg.Rect(0,0,info.current_w,info.current_h)

def init(size, position=None):
    """
    Return a Rect for use as the screen size, and optionally set the
    environment variable for positioning the window position.

    :param size: (width, height) size of display.
    :param position': name of rect attribute to align window rect against desktop.
    """
    rect = pg.Rect((0,0),size)

    if position is not None:
        desktop_rect = get_desktop_rect()
        setattr(rect, position, getattr(desktop_rect, position))
        set_position(rect.topleft)

    return rect

def set_position(position):
    """
    Set the top-left position of the window. Call before
    `pygame.display.set_mode`.
    """
    x, y = position
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (x, y)
