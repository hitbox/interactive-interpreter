import unittest

from interpreter.textbox import Textbox

class TestTextbox(unittest.TestCase):

    def setUp(self):
        self.textbox = Textbox()

    def test_editing(self):
        self.textbox.write("abc")
        self.assertEqual(self.textbox.value, "abc")

        # backspace one character at a time
        self.textbox.backspace()
        self.assertEqual(self.textbox.value, "ab")

        # ditto
        self.textbox.backspace()
        self.assertEqual(self.textbox.value, "a")

        # insert after "a"
        self.textbox.write("abc")
        self.assertEqual(self.textbox.value, "aabc")

        self.textbox.move_left(2)
        # insert before the "b"
        self.textbox.write("xyz")
        self.assertEqual(self.textbox.value, "aaxyzbc")

        # move to end
        self.textbox.move_end()
        self.assertEqual(self.textbox.position, len(self.textbox.value))

        # backspace several chars
        self.textbox.backspace(3)
        self.assertEqual(self.textbox.value, "aaxy")

        self.textbox.clear()
        self.assertEqual(self.textbox.value, "")


if __name__ == '__main__':
    unittest.main()
