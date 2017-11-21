from .base import Sprite

class BakedSprite(Sprite):

    def __init__(self, image, *groups, position=None):
        super().__init__(*groups)
        self.image = image
        if position is None:
            position = {}
        self.rect = self.image.get_rect(**position)
