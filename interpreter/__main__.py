import pygame as pg

from . import window
from .screen import Screen
from .engine import Engine

# set window aligned midright to desktop
desktop_rect = window.get_desktop_rect()
display_rect = pg.Rect(0,0,1000,900)
display_rect.midright = desktop_rect.midright
display_rect.left -= 10

window.set_position(display_rect.topleft)

display = Screen(display_rect.size)

from .scenes import ReadlineScene

e = Engine(display)
e.run(ReadlineScene())
