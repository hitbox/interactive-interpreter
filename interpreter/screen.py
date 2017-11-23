import pygame as pg

class Screen(object):

    def __init__(self, size):
        self.display = pg.display.set_mode(size)
        self.rect = self.display.get_rect()
        self.background = self.display.copy()
        self.background.fill((0,0,0))

    def clear(self):
        self.display.blit(self.background, (0,0))

    def flip(self):
        pg.display.flip()
