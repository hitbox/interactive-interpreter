import unittest

from interpreter.readline import Readline

class TestReadline(unittest.TestCase):

    def setUp(self):
        self.readline = Readline()

    def test_editing(self):
        self.readline.write("abc")
        self.assertEqual(self.readline.value, "abc")

        # backspace one character at a time
        self.readline.backspace()
        self.assertEqual(self.readline.value, "ab")

        # ditto
        self.readline.backspace()
        self.assertEqual(self.readline.value, "a")

        # insert after "a"
        self.readline.write("abc")
        self.assertEqual(self.readline.value, "aabc")

        self.readline.move_left(2)
        # insert before the "b"
        self.readline.write("xyz")
        self.assertEqual(self.readline.value, "aaxyzbc")

        # move to end
        self.readline.move_end()
        self.assertEqual(self.readline.position, len(self.readline.value))

        # backspace several chars
        self.readline.backspace(3)
        self.assertEqual(self.readline.value, "aaxy")

        self.readline.clear()
        self.assertEqual(self.readline.value, "")

    def test_history(self):
        self.readline.write("abc")
        value = self.readline.submit()
        self.assertEqual(value, "abc")

        self.readline.write("123")
        value = self.readline.submit()
        self.assertEqual(value, "123")

        self.readline.write("foo")
        value = self.readline.submit()
        self.assertEqual(value, "foo")

        self.readline.write("bar")
        value = self.readline.submit()
        self.assertEqual(value, "bar")

        self.readline.write("line left unsubmitted")

        # move up history
        value = self.readline.history_up()
        self.assertEqual(value, "bar")

        value = self.readline.history_up()
        self.assertEqual(value, "foo")

        value = self.readline.history_up()
        self.assertEqual(value, "123")

        value = self.readline.history_up()
        self.assertEqual(value, "abc")

        # start of history
        value = self.readline.history_up()
        self.assertEqual(value, "abc")

        # move down history
        value = self.readline.history_down()
        self.assertEqual(value, "123")

        value = self.readline.history_down()
        self.assertEqual(value, "foo")

        value = self.readline.history_down()
        self.assertEqual(value, "bar")

        # end of history, should bring back "current" line
        value = self.readline.history_down()
        self.assertEqual(value, "line left unsubmitted")


if __name__ == '__main__':
    unittest.main()
