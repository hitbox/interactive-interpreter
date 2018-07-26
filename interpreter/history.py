class History(object):

    def __init__(self, initial=None):
        if initial is None:
            initial = []
        self.lines = initial
        self.index = None

    def add(self, line):
        if line in self.lines:
            # move it to the bottom (nearest)
            self.lines.remove(line)
        self.lines.append(line)

    def down(self):
        if self.index is None:
            return
        if self.lines and self.index + 1 < len(self.lines):
            self.index += 1
            return self.lines[self.index]

    def reset_index(self):
        self.index = None

    def up(self):
        if not self.lines:
            return
        if self.index is None:
            self.index = len(self.lines) - 1
        elif self.index - 1 >= 0:
            self.index += -1
        return self.lines[self.index]
