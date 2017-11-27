from .history import History

class Readline(object):

    def __init__(self, value=""):
        self.value = value
        # backup value when moving through history, using None to indicate
        # we're back in the current line
        self._value = None
        self.position = len(self.value)
        self.history = History()

    def _restore_value(self):
        if self._value is not None:
            self.value = self._value
            self.move_end()
            self._value = None

    def _save_value(self):
        if self._value is None:
            self._value = self.value

    def backspace(self, nchars=1):
        if not self.value:
            return
        chars = list(self.value)
        self.value = "".join(chars[:self.position - nchars] + chars[self.position:])
        self.position -= nchars

    def clear(self):
        self.value = ""
        self.position = 0

    def delete(self):
        self.value = "".join(c for i, c in enumerate(self.value) if i != self.position)

    def history_down(self):
        next_ = self.history.down()
        if next_:
            self._save_value()
            self.value = next_
            self.move_end()
        else:
            self._restore_value()
            self.history.reset_index()
        return self.value

    def history_up(self):
        next_ = self.history.up()
        if next_:
            self._save_value()
            self.value = next_
            self.move_end()
        return self.value

    def history_save(self):
        self.history.add(self.value)

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

    def submit(self, save_history=True):
        if save_history:
            self.history_save()
        self.history.reset_index()
        rv = self.value
        self.clear()
        return rv

    def write(self, data):
        chars = list(self.value)
        chars = chars[:self.position] + list(data) + chars[self.position:]
        self.value = "".join(chars)
        self.position += len(data)
