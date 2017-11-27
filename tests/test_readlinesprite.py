import unittest

import pygame as pg

from interpreter.engine import g
from interpreter.sprites.readline import ReadlineSprite

class DummyEngine:

    def emit(self, whatever):
        pass


g.engine = DummyEngine()

class TestReadlineSprite(unittest.TestCase):

    def setUp(self):
        self.rlsprite = ReadlineSprite(">>>", pg.Rect(0,0,256,240))

    @unittest.skip("TODO: test caret rect is calculated correctly.")
    def test_get_caret_rect(self):
        # This was created to debug why `history_down` was eventually causing
        # `get_caret_rect` to fail. Keeping it around in case I come up with a
        # good way to test the rect returned by `get_caret_rect`.

        self.rlsprite.write("foo")
        self.assertEqual(self.rlsprite.submit(), "foo")

        print(self.rlsprite.get_caret_rect())

        self.rlsprite.readline.history_up()
        print(self.rlsprite.get_caret_rect())

        self.rlsprite.readline.history_down()
        print(self.rlsprite.readline.value)
        print(self.rlsprite.get_caret_rect())


if __name__ == "__main__":
    unittest.main()
