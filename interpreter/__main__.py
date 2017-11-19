import pygame as pg

from . import screen, window
from .engine import Engine

rect = window.init((640,480), position='midright')

screen = screen.Screen(rect.size)

from .scenes import ConsoleScene

e = Engine(screen)
e.run(ConsoleScene())
