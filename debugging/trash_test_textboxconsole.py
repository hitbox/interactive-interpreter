import io
import string
import textwrap
import unittest

import pygame as pg
pg.display.init()

from interpreter.console import StreamConsole
from interpreter.sprites import ReadlineSprite

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

def text2events(text):
    for letter in text:
        event = letter2keydown[letter]
        yield event

class TestTextboxConsole(unittest.TestCase):

    def setUp(self):
        self.console_output = io.StringIO()
        self.console = StreamConsole(self.console_output, locals=dict())
        self.rlsprite = ReadlineSprite(">>>", pg.Rect(0,0,0,0))

    def _keydown_hook(self, event):
        "Send pygame keydown events to the rlsprite as strings."
        self.rlsprite.write(event.unicode)

    def _pygame_event_loop(self, events, return_hook, keydown_hook=None):
        """
        Simple python main loop that posts `events` to the queue one at a time,
        reads them back off, and calls the return and keydown hooks. This is a
        way to simulated the user typing and creating events for the loop to
        consume.
        :param events: The events to post to queue. Meant to be the output of
                       text2events.
        :param return_hook: Called when return is pressed.
        :param keydown_hook: Optional. Called on every keydown event. Defaults
                             to writing the unicode attribute to the rlsprite.
        """
        if keydown_hook is None:
            keydown_hook = self._keydown_hook
        pg.event.pump()
        pg.event.set_allowed(pg.KEYDOWN)
        for simulated_event in events:
            pg.event.post(simulated_event)
            for event in pg.event.get():
                print(event)
                if event.type == pg.KEYDOWN:
                    self.rlsprite.on_keydown(event)
                    if event.key == pg.K_RETURN:
                        return_hook(event)

    def _test_pygame_event_loop(self, source, nmore, expected):
        """
        :param source: Python source code sent character by character, through
                       a pygame event loop, to the console.
        :param nmore: Expected number of mores returned by pushing to the
                      console. Remember, this should be the number of newlines
                      in source minus one, because the last line should cause
                      compilable code.
        :param expected: The expected string output of the ran code.
        """
        self.nmore = nmore
        def return_hook(event):
            """
            A return hook that verifies the number of more console pushes
            occurs and the console_output.
            """
            more = self.console.push(self.rlsprite.readline.value)
            self.assertEqual(bool(self.nmore), more)
            self.nmore -= 1
            # nmore goes below zero for zero expected mores
            if self.nmore <= 0:
                self.assertEqual(self.console_output.getvalue(), expected)
        events = text2events(source)
        self._pygame_event_loop(events, return_hook)

    def test_pygame_console_single_line(self):
        """
        Test that `dir()` returns what is expected.
        """
        self._test_pygame_event_loop("dir()\n", 0, "['__builtins__']")

    def test_pygame_console_multiple_lines(self):
        """
        Testing creating a class, instantiating it, and getting the value of
        it's attribute back like an interpreter does.
        """
        # should declare a class returning nothing
        self._test_pygame_event_loop(textwrap.dedent(
            """class C:
                   def __init__(self):
                       self.a = 1234567890
                \n"""), # NOTE: two newlines to complete class declaration
            3, "")
        # should make an instance of the class, returning nothing
        self._test_pygame_event_loop("c = C()\n", 0, "")
        # should write out the value of the `a` attribute of the instance of the class
        self._test_pygame_event_loop("c.a\n", 0, "1234567890")


if __name__ == "__main__":
    unittest.main()
