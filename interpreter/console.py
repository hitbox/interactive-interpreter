import code

import pygame as pg

class Console(code.InteractiveInterpreter):

    def __init__(self, spritetextbox, locals=None, filename='<console>'):
        super().__init__(locals)
        self.spritetextbox = spritetextbox
        self.filename = filename
        self.resetbuffer()

    def on_keydown(self, event):
        self.spritetextbox.on_keydown(event)
        if event.key == pg.K_RETURN:
            line = self.spritetextbox.textbox.value
            self.spritetextbox.textbox.value = ''
            more = self.push(line)

    def push(self, line):
        self.buffer.append(line)
        source = '\n'.join(self.buffer)
        more = self.runsource(source, self.filename)
        if not more:
            self.resetbuffer()
        return more

    def resetbuffer(self):
        self.buffer = []

    def write(self, data):
        self.spritetextbox.textbox.value += data
