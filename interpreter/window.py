import os

import pygame as pg

def get_desktop_rect():
    """
    Return the desktop size as Rect. Call before `pygame.display.set_mode`.
    """
    info = pg.display.Info()
    return pg.Rect(0,0,info.current_w,info.current_h)

def set_position(position):
    """
    Set the top-left position of the window. Call before
    `pygame.display.set_mode`.
    """
    x, y = position
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (x, y)
