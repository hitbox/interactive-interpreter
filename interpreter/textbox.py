import pygame as pg

class Textbox(object):

    def __init__(self):
        self.value = ''

    def on_keydown(self, event):
        if event.key == pg.K_BACKSPACE:
            chars = list(self.value)
            try:
                chars.pop()
            except IndexError:
                pass
            else:
                self.value = ''.join(chars)
        else:
            self.value += event.unicode
