import pygame as pg

class Screen(object):

    def __init__(self, size):
        self.display = pg.display.set_mode(size)
        self.rect = self.display.get_rect()

    def clear(self):
        self.display.fill((0,0,0))

    def flip(self):
        pg.display.flip()
