from math import fabs
from operator import ge, le, gt, lt

class Tween(object):

    def __init__(self, start, end, steps):
        self.start = start
        self.end = end
        self.steps = steps

        self.start = float(self.start)
        self.end = float(self.end)
        self.steps = float(self.steps)

        self.current = self.start
        self.step = fabs(self.start - self.end) / self.steps

        if self.end < self.start:
            self.step *= -1
            self.cmpfunc = gt
        else:
            self.cmpfunc = lt

    def __iter__(self):
        return self

    def __next__(self):
        if self.cmpfunc(self.current, self.end):
            rv = self.current
            self.current += self.step
            return rv

        elif self.current != self.end:
            self.current = self.end
            return self.end

        raise StopIteration


class TweenColor(object):
    """
    An iterator from one color to another.
    """

    def __init__(self, start, end, steps):
        self.start = start
        self.end = end
        self.steps = steps

        if len(self.start) == 4:
            r1, b1, g1, a1 = self.start
        else:
            r1, b1, g1 = self.start
            a1 = 255

        if len(self.end) == 4:
            r2, b2, g2, a2 = self.end
        else:
            r2, b2, g2 = self.end
            a2 = 255

        self.reds = Tween(r1, r2, self.steps)
        self.blues = Tween(b1, b2, self.steps)
        self.greens = Tween(g1, g2, self.steps)
        self.alphas = Tween(a1, a2, self.steps)

    def __iter__(self):
        return self

    def __next__(self):
        exhausted = [False] * 4
        try:
            r = next(self.reds)
        except StopIteration:
            r = self.reds.end
            exhausted[0] = True
        try:
            b = next(self.blues)
        except StopIteration:
            b = self.blues.end
            exhausted[1] = True
        try:
            g = next(self.greens)
        except StopIteration:
            g = self.greens.end
            exhausted[2] = True
        try:
            a = next(self.alphas)
        except StopIteration:
            a = self.alphas.end
            exhausted[3] = True

        if all(exhausted):
            raise StopIteration
        else:
            return (r, g, b, a)
