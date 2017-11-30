from collections import deque

from interpreter.sprites import Sprite
from interpreter.tween import Tween

class MovingSprite(Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)
        self.paths = deque()

    def moveto(self, target, steps):
        lastx, lasty = None, None

        if self.paths:
            lastxtween, lastytween = self.paths[0]
            lastx, lasty = map(int, (lastxtween.end, lastytween.end))
        else:
            xtween = getattr(self, "xtween", None)
            ytween = getattr(self, "ytween", None)
            if xtween:
                lastx = int(xtween.end)
            else:
                lastx = self.rect.x
            if ytween:
                lasty = int(ytween.end)
            else:
                lasty = self.rect.y

        xtween = Tween(lastx, target.x, steps)
        ytween = Tween(lasty, target.y, steps)
        self.paths.appendleft((xtween, ytween))

    def movetos(self, targets, steps):
        for target in targets:
            self.moveto(target, steps)

    def update_moveto(self):
        hasxtween, hasytween = hasattr(self, "xtween"), hasattr(self, "ytween")
        if hasxtween:
            try:
                self.rect.x = next(self.xtween)
            except StopIteration:
                self.rect.x = self.xtween.end
                del self.xtween

        if hasytween:
            try:
                self.rect.y = next(self.ytween)
            except StopIteration:
                self.rect.y = self.ytween.end
                del self.ytween

        if not hasxtween and not hasytween and self.paths:
            self.xtween, self.ytween = self.paths.pop()

    def update(self):
        self.update_moveto()
