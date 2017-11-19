from .group import Group

from .sprites import SpriteConsole

class ConsoleScene(Group):

    def __init__(self, locals=None):
        super().__init__()

        self.console = SpriteConsole(locals)
        self.add(self.console)
