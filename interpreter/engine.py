import logging
from collections import defaultdict

import pygame as pg

from .clock import Clock
from .events import ReadlineEvent
from .globals import g
from .screens import Screen

class Engine(object):

    def __init__(self, screen):
        g.engine = self
        g.clock = self.clock = Clock()
        g.screen = self.screen = screen
        pg.key.set_repeat(150, 50)
        self.is_running = False

        self.listeners = defaultdict(list)

    def emit(self, event):
        pg.event.post(event)

    def handle(self, event):
        if event.type == pg.QUIT:
            self.is_running = False
        elif event.type in self.listeners:
            for callback in self.listeners[event.type]:
                callback(event)

    def listen(self, type, f):
        self.listeners[type].append(f)

    def stop(self):
        pg.event.post(pg.event.Event(pg.QUIT))

    def run(self, scene):
        self.scene = scene
        self.is_running = True
        while self.is_running:
            g.elapsed = g.clock.tick()
            for event in pg.event.get():
                self.handle(event)

            self.scene.update()

            self.screen.clear()
            self.scene.draw(self.screen.display)
            self.screen.flip()
        logging.getLogger('interpreter.engine').info('engine shut down')
