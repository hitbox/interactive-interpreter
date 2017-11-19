import pygame as pg

class Clock(object):

    def __init__(self, framerate=60):
        self._clock = pg.time.Clock()
        self.framerate = framerate

    def tick(self):
        return self._clock.tick(self.framerate)
