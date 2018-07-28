import pygame as pg

from ..globals import g
from ..rect import Rect
from .base import Sprite
from .draggable import Draggable

def opposite(rect_attr):
    if 'top' in rect_attr:
        key = 'bottom'
    elif 'bottom' in rect_attr:
        key = 'top'

    if 'left' in rect_attr:
        key += 'right'
    elif 'right' in rect_attr:
        key += 'left'

    return key

class RectSprite(Rect, Sprite):

    def __init__(self,
            size,
            *groups,
            color = (255,255,255),
            line_width = 1,
        ):
        super(Rect, self).__init__((0, 0), size)
        super(Sprite, self).__init__(*groups)
        self.rect = self
        self.size = size
        self.color = color
        self.line_width = line_width

        self.handle_size = (50, 50)
        self.handles = {
            attr: Draggable(getattr(self, attr), self.handle_size)
            for attr in ['topleft', 'topright', 'bottomright', 'bottomleft']
        }

        self.links = {
            self.handles['topleft']: [
                (self.handles['topright'], 'y'),
                (self.handles['bottomleft'], 'x'),
            ],

            self.handles['topright']: [
                (self.handles['topleft'], 'y'),
                (self.handles['bottomright'], 'x'),
            ],

            self.handles['bottomright']: [
                (self.handles['topright'], 'x'),
                (self.handles['bottomleft'], 'y'),
            ],

            self.handles['bottomleft']: [
                (self.handles['bottomright'], 'y'),
                (self.handles['topleft'], 'x'),
            ],
        }

        g.engine.listen(pg.USEREVENT, self.on_userevent)

    @property
    def image(self):
        return self.render(self.color, self.line_width)

    def on_userevent(self, event):
        """
        On a 'moved' event, update the position of this object's attribute that
        the handle is controlling.
        """
        if event.subtype == 'moved' and event.target in self.handles.values():
            for attr, handle in self.handles.items():
                if handle is event.target:
                    break
            setattr(self, attr, handle.rect.center)
            self.update_linked_attributes(handle)

    def update_linked_attributes(self, handle):
        """
        Updated the linked attributes of the handle.
        """
        for linked_handle, linked_attr in self.links[handle]:
            setattr(
                linked_handle.rect,
                linked_attr,
                getattr(
                    handle.rect,
                    linked_attr
                )
            )
            if linked_attr == 'x':
                self.height = abs(linked_handle.rect.centery - handle.rect.centery)
            elif linked_attr == 'y':
                self.width = abs(linked_handle.rect.centerx - handle.rect.centerx)

    def move_ip(self, x, y):
        super().move_ip(x, y)
        handle = self.handles['topleft']
        handle.rect.center = self.topleft
        self.update_linked_attributes(handle)

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))
