import pygame as pg

from . import screens
from .engine import Engine
from .globals import g
from .scenes import ReadlineScene

screen = screens.desktop_aligned_midright((1000,900))
screen.background.fill((31,31,31))
engine = Engine(screen)
scene = ReadlineScene(g.screen.rect.inflate(-25, -25),
                      dict(g=g, pg=pg),
                      banner=ReadlineScene.banner + "\nDemonstration of a console in pygame.")
engine.run(scene)
