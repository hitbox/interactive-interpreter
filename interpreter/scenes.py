import io

import pygame as pg

from .globals import g
from .font import Font
from .group import Group
from .console import StreamConsole

from .sprites import BakedSprite, FramesPerSecondSprite, ReadlineSprite

class ReadlineScene(Group):

    def __init__(self):
        super().__init__()

        self.lines = []
        self.font = Font()

        self.inside = g.screen.rect.inflate(-100, -100)

        self.padding = 10

        self.readlinesprite = ReadlineSprite(">>> ", self.inside)

        add_history = self.readlinesprite.readline.history.add
        for command in ["dir()", "s.rect.topright = fps.rect.topright"]:
            add_history(command)

        topleft = (g.screen.rect.left + self.padding,
                   g.screen.rect.top + self.padding)
        self.readlinesprite.rect.topleft = topleft
        self.add(self.readlinesprite)
        self.bakes = []
        self.reverse = []

        fps = FramesPerSecondSprite()
        fps.rect.topright = g.screen.rect.topright

        s = BakedSprite(fps.image.copy())
        s.image.fill((255,25,25))
        s.rect.center = g.screen.rect.center

        self.add(s, fps)

        ctx = dict(g=g, screen=g.screen, engine=g.engine, scene=self,
                   BakedSprite=BakedSprite, pg=pg, s=s, bakes=self.bakes,
                   FramesPerSecondSprite=FramesPerSecondSprite, fps=fps,
                   quit=g.engine.stop)
        self.console = StreamConsole(io.StringIO(), locals=ctx)

        # XXX: quick-dirty banner
        #      uses self.readlinesprite's rect to start
        self._bake_output("Pygame Interactive Interpreter")
        self._bake_output("Close window or `engine.stop()` or `quit()` or CTRL+D to quit")
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
        self.reverse.insert(0, baked)

    def _reflow_up(self):
        self.bakes[-1].rect.bottomleft = self.readlinesprite.rect.topleft
        for b1, b2 in zip(self.reverse[:-1], self.reverse[1:]):
            b2.rect.bottomleft = b1.rect.topleft

    def _keep_readline_on_screen(self):
        if self.readlinesprite.rect.bottom > g.screen.rect.bottom:
            self.readlinesprite.rect.bottom = g.screen.rect.bottom - self.padding
            self._reflow_up()

    def on_userevent(self, event):
        if event.subtype != "readline":
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
                    self._bake_output(self.readlinesprite.prompt + output)
                self.readlinesprite.readline.history.add(event.value)
                self.readlinesprite.prompt = ">>> "
                self.readlinesprite.render()

            last_bake = self.bakes[-1]
            self.readlinesprite.rect.topleft = last_bake.rect.bottomleft

        self._keep_readline_on_screen()
