import pygame as pg

from . import screen
from .engine import Engine
from .scenes import ReadlineScene

e = Engine(screen.desktop_aligned((1000,900), position=dict(midright="midright")))
e.run(ReadlineScene())
