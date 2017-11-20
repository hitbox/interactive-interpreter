import io
import string
import unittest

import pygame as pg
pg.display.init()

from interpreter.console import StreamedConsole
from interpreter.textbox import Textbox

def keydown_event(data):
    return pg.event.Event(pg.KEYDOWN, data)

letter2keydown = {}
for letter in string.ascii_letters + string.digits:
    key = getattr(pg, "K_" + letter.lower())
    if letter.isupper():
        mod = pg.KMOD_SHIFT
    else:
        mod = pg.KMOD_NONE
    letter2keydown[letter] = keydown_event(dict(key=key, unicode=letter, mod=mod))

for letter, key in [("\n", pg.K_RETURN), ("(", pg.K_LEFTPAREN),
                    (")", pg.K_RIGHTPAREN), (" ", pg.K_SPACE),
                    (":", pg.K_COLON), ("\t", pg.K_TAB), (".", pg.K_PERIOD),
                    ("_", pg.K_UNDERSCORE), ("=", pg.K_EQUALS)]:
    letter2keydown[letter] = keydown_event(dict(key=key, unicode=letter, mod=pg.KMOD_NONE))

def line2events(line):
    for letter in line:
        event = letter2keydown[letter]
        yield event

class TestTextboxConsole(unittest.TestCase):

    def setUp(self):
        self.output = io.StringIO()
        self.console = StreamedConsole(self.output, locals=dict())
        self.textbox = Textbox()

    def _keydown_hook(self, event):
        self.textbox.write(event.unicode)

    def _pygame_event_loop(self, events, return_hook, keydown_hook=None):
        if keydown_hook is None:
            keydown_hook = self._keydown_hook
        pg.event.pump()
        pg.event.set_allowed(pg.KEYDOWN)
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    keydown_hook(event)
                    if event.key == pg.K_RETURN:
                        return_hook(event)
            try:
                pg.event.post(next(events))
            except StopIteration:
                break

    def test_pygame_console_single_line(self):
        keydowns = line2events("dir()\n")

        def return_hook(event):
            more = self.console.push(self.textbox.value)
            self.assertFalse(more)

            out = self.output.getvalue()
            self.assertEqual(out, "['__builtins__']")
        self._pygame_event_loop(keydowns, return_hook)

    def test_pygame_console_multiple_lines(self):
        keydowns = line2events("class C:\n def __init__(self):\n  self.a = 1\n")

        self.more_countdown = 2
        def return_hook(event):
            lines = self.textbox.value.splitlines()
            lastline = lines[-1]
            more = self.console.push(lastline.rstrip("\n"))

            print((lines, self.console.buffer))

            self.assertEqual(bool(self.more_countdown), more)
            self.more_countdown -= 1

            if not self.more_countdown:
                out = self.output.getvalue()
                print("out: %s" % out)
                self.assertEqual(out, "['__builtins__']\n")
        self._pygame_event_loop(keydowns, return_hook)


if __name__ == "__main__":
    unittest.main()
