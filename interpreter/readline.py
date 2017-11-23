class History(object):

    def __init__(self, initial=None):
        if initial is None:
            initial = []
        self.lines = initial
        self.index = 0

    def add(self, line):
        self.lines.append(line)

    def down(self):
        if self.lines and self.index + 1 < len(self.lines):
            self.index += 1
            return self.lines[self.index]

    def up(self):
        if self.lines and self.index - 1 > -1:
            self.index += -1
            return self.lines[self.index]


class Readline(object):

    def __init__(self, value=""):
        self.value = value
        self.position = len(self.value)
        self.history = History()

    def backspace(self, nchars=1):
        if not self.value:
            return
        chars = list(self.value)
        self.value = "".join(chars[:self.position - nchars] + chars[self.position:])
        self.position -= nchars

    def clear(self):
        self.value = ""
        self.position = 0

    def history_down(self):
        next_ = self.history.down()
        if next_:
            self.value = next_
            self.position = len(self.value)

    def history_up(self):
        next_ = self.history.up()
        if next_:
            self.value = next_
            self.position = len(self.value)

    def last_line(self):
        if not self.value:
            return ""
        return self.value.splitlines()[-1]

    def move_end(self):
        self.position = len(self.value)

    def move_left(self, nchars=1):
        self.position -= nchars
        if self.position < 0:
            self.position = 0

    def move_right(self, nchars=1):
        self.position += nchars
        if self.position > len(self.value):
            self.position = len(self.value)

    def write(self, data):
        chars = list(self.value)
        chars = chars[:self.position] + list(data) + chars[self.position:]
        self.value = "".join(chars)
        self.position += len(data)
