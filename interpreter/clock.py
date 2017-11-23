import pygame as pg

class Clock(object):

    def __init__(self, framerate=60):
        self._clock = pg.time.Clock()
        self.framerate = framerate

    def get_fps(self):
        return self._clock.get_fps()

    def tick(self):
        return self._clock.tick(self.framerate)
