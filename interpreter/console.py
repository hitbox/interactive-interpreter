import code
import contextlib
import io
import sys

import pygame as pg

class StreamedConsole(code.InteractiveInterpreter):

    def __init__(self, output, locals=None, filename="<console>"):
        super().__init__(locals)
        self.filename = filename
        self.resetbuffer()
        self.output = output

    def push(self, line):
        self.buffer.append(line)

        temp = io.StringIO()
        with contextlib.redirect_stdout(temp):
            more = self.runsource(self.source(), self.filename)

        if not more:
            self.resetbuffer()
            self.output.write(temp.getvalue())
        return more

    def resetbuffer(self):
        self.buffer = []

    def source(self):
        return "\n".join(self.buffer)

    def write(self, data):
        self.output.write(data)
