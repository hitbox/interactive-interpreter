import pygame as pg

from . import screen, window
from .engine import Engine, g

desktop_rect = window.get_desktop_rect()
display_rect = pg.Rect(0,0,1000,900)
display_rect.midright = desktop_rect.midright
display_rect.left -= 10

window.set_position(display_rect.topleft)

screen = screen.Screen(display_rect.size)

from .scenes import ConsoleScene

e = Engine(screen)
e.run(ConsoleScene(dict(g=g)))
