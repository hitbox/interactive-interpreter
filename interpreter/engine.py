import pygame as pg

from .clock import Clock
from .screen import Screen

class g:

    clock = None
    engine = None
    screen = None


class Engine(object):

    def __init__(self, screen):
        g.engine = self
        g.clock = self.clock = Clock()
        g.screen = self.screen = screen
        pg.key.set_repeat(150, 50)
        self.is_running = False

    def handle(self, event):
        if event.type == pg.QUIT:
            self.is_running = False
        elif event.type == pg.KEYDOWN:

            # TODO: handle keydown that quits better
            if event.key in (pg.K_q, pg.K_ESCAPE):
                pg.event.post(pg.event.Event(pg.QUIT))

            else:
                for sprite in self.scene.sprites():
                    if hasattr(sprite, 'on_keydown'):
                        sprite.on_keydown(event)

    def run(self, scene):
        self.scene = scene
        self.is_running = True
        while self.is_running:
            for event in pg.event.get():
                self.handle(event)

            self.scene.update()

            self.screen.clear()
            self.scene.draw(self.screen.display)
            self.screen.flip()
