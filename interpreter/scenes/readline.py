import io

import pygame as pg

from ..console import StreamConsole
from ..font import Font
from ..globals import g
from ..sprites import BakedSprite, ReadlineSprite

from .base import BaseScene

class ReadlineScene(BaseScene):
    """
    """

    banner = ("Pygame Interactive Interpreter\n"
              "Close window or `engine.stop()` or `quit()` or CTRL+D to quit.")

    def __init__(self, inside, context=None, banner=None):
        """
        :param inside: rect to keep console in.
        :param type: interpreter.rect.Rect

        :param context: console locals.
        :param banner: override default banner.
        """
        super().__init__()

        self.lines = []
        self.font = Font()

        self.inside = inside
        self.add(self.inside)
        for handle in self.inside.handles.values():
            self.add(handle)

        self.readlinesprite = ReadlineSprite(">>> ", self.inside)

        #self.readlinesprite.rect.topleft = self.inside.topleft
        self.add(self.readlinesprite)
        self.bakes = []
        self.history = []

        self.console = StreamConsole(io.StringIO(), locals=context)

        if banner is None:
            banner = self.banner

        # XXX: quick-dirty banner
        #      uses self.readlinesprite's rect to start
        for line in banner.splitlines():
            self._bake_output(line)
        self.readlinesprite.rect.topleft = self.bakes[-1].rect.bottomleft

        g.engine.listen(pg.USEREVENT, self.on_userevent)

    def _bake_output(self, text):
        if self.bakes:
            last_bake = self.bakes[-1]
            position = dict(topleft=last_bake.rect.bottomleft)
        else:
            position = dict(topleft=self.inside.topleft)
        image = self.font.render(text, self.inside)
        baked = BakedSprite(image, self, position=position)
        self.add(baked)
        self.bakes.append(baked)
        self.history.insert(0, baked)

    def _reflow_up(self):
        self.bakes[-1].rect.bottomleft = self.readlinesprite.rect.topleft
        for b1, b2 in zip(self.history[:-1], self.history[1:]):
            b2.rect.bottomleft = b1.rect.topleft
        removes = []
        for baked in self.bakes:
            if baked.rect.top < self.inside.top:
                removes.append(baked)
        for baked in removes:
            self.remove(baked)
            self.bakes.remove(baked)
            self.history.remove(baked)

    def _keep_readline_on_screen(self):
        if self.readlinesprite.rect.bottom > self.inside.bottom:
            self.readlinesprite.rect.bottom = self.inside.bottom
            self._reflow_up()

    def on_userevent(self, event):
        if not hasattr(event, 'subtype') or event.subtype != "readline":
            return

        if event.action == "submit":
            # a line has been read by readlinesprite
            self._bake_output(self.readlinesprite.prompt + event.value)

            more = self.console.push(event.value)
            if more:
                self.readlinesprite.prompt = "... "
                self.readlinesprite.render()
            else:
                # console consumed whatever was given
                output = self.console.stream.getvalue()
                if output:
                    self.console.stream = io.StringIO()
                    for line in output.splitlines():
                        self._bake_output(line)
                self.readlinesprite.readline.history.add(event.value)
                self.readlinesprite.prompt = ">>> "
                self.readlinesprite.render()

            last_bake = self.bakes[-1]
            #self.readlinesprite.rect.topleft = last_bake.rect.bottomleft

        self._keep_readline_on_screen()
