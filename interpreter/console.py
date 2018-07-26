import code
import contextlib
import io

class StreamConsole(code.InteractiveInterpreter):
    """
    A console that writes stdout of runsource to a string, `stream`.
    """

    def __init__(self, stream, locals=None, filename="<console>"):
        super().__init__(locals)
        self.filename = filename
        self.resetbuffer()
        self.stream = stream

    def push(self, line):
        self.buffer.append(line)

        temp = io.StringIO()
        with contextlib.redirect_stdout(temp):
            more = self.runsource(self.source(), self.filename)

        if not more:
            self.resetbuffer()
            self.write(temp.getvalue().rstrip("\n"))
        return more

    def resetbuffer(self):
        self.buffer = []

    def source(self):
        return "\n".join(self.buffer)

    def write(self, data):
        self.stream.write(data)
