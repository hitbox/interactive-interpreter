class Textbox(object):

    def __init__(self, value=''):
        self.value = value
        self.position = len(self.value)

    def backspace(self, nchars=1):
        chars = list(self.value)
        self.value = "".join(chars[:self.position - nchars] + chars[self.position:])
        self.position -= nchars

    def clear(self):
        self.value = ''
        self.position = 0

    def last_line(self):
        if not self.value:
            return ''
        return self.value.splitlines()[-1]

    def move_end(self):
        self.position = len(self.value)

    def move_left(self, nchars=1):
        self.position -= nchars

    def move_right(self, nchars=1):
        self.position += nchars

    def write(self, data):
        chars = list(self.value)
        chars = chars[:self.position] + list(data) + chars[self.position:]
        self.value = "".join(chars)
        self.position += len(data)
