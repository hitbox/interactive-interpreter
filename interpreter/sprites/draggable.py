import pygame as pg

from .base import Sprite
from ..globals import g

class Draggable(Sprite):

    def __init__(self,
            center,
            size,
            *groups,
            color = (255,0,0)
        ):
        super().__init__(*groups)
        self.center = center
        self.size = size
        assert color is not None
        self.color = color
        topleft = self.center[0] - self.size[0] / 2, self.center[1] - self.size[0] / 2
        self.rect = pg.Rect(topleft, size)
        self.image = pg.Surface(self.rect.size, flags=pg.SRCALPHA)
        pg.draw.circle(
            self.image,
            self.color,
            self.image.get_rect().center,
            int(min(self.rect.size) / 2),
            1
        )

        self.hovering = False
        self.dragging = False

        g.engine.listen(pg.MOUSEMOTION, self.on_mousemotion)
        g.engine.listen(pg.MOUSEBUTTONDOWN, self.on_mousebuttondown)
        g.engine.listen(pg.MOUSEBUTTONUP, self.on_mousebuttonup)

    def on_mousemotion(self, event):
        self.hovering = self.rect.collidepoint(event.pos)
        if self.dragging:
            self.rect.move_ip(event.rel)
            self.center = self.rect.center
            self.size = self.rect.size
            g.engine.emit(
                pg.event.Event(
                    pg.USEREVENT,
                    subtype = 'moved',
                    target = self,
                )
            )

    def on_mousebuttondown(self, event):
        if self.hovering and event.button == 1:
            self.dragging = True

    def on_mousebuttonup(self, event):
        if event.button == 1:
            self.dragging = False
