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
