
import pygame as pg

from interpreter import screens
from interpreter.engine import Engine
from interpreter.globals import g
from interpreter.scenes import BaseScene, ReadlineScene
from interpreter.sprites import FramesPerSecondSprite, Sprite
from interpreter.utils import positioned

from .staging.sprites import MovingSprite

class MovingSpriteScene(BaseScene):

    def __init__(self):
        super().__init__()

        leftside = g.screen.rect.copy()
        leftside.width /= 2

        rightside = g.screen.rect.copy()
        rightside.width /= 2
        rightside.topright = g.screen.rect.topright

        pg.draw.rect(g.screen.background,(90,90,90),leftside,1)
        pg.draw.rect(g.screen.background,(90,90,90),rightside,1)

        sprite = MovingSprite()
        sprite.image = pg.Surface((100, 50))
        sprite.image.fill((200,100,100))
        sprite.rect = sprite.image.get_rect()
        self.add(sprite)

        fps = FramesPerSecondSprite()
        fps.rect.topright = leftside.topright
        self.add(fps)

        steps = 60

        context = dict(g=g, pg=pg, sprite=sprite, s=sprite, positioned=positioned,
                       leftside=leftside, rightside=rightside, steps=steps)

        banner = ReadlineScene.banner + "\nUp/down for example commands to move the sprite on the right."
        self.subscene = ReadlineScene(leftside.inflate(-100, -100), context, banner=banner)
        pg.draw.rect(g.screen.background,(90,200,90),self.subscene.inside,1)

        sprite.rect.center = rightside.center
        sprite.moveto(positioned(sprite.rect, midright=rightside.midright), steps)
        sprite.moveto(positioned(sprite.rect, topright=rightside.topright), steps)
        sprite.moveto(positioned(sprite.rect, topleft=rightside.topleft), steps)
        sprite.moveto(positioned(sprite.rect, bottomleft=rightside.bottomleft), steps)
        sprite.moveto(positioned(sprite.rect, bottomright=rightside.bottomright), steps)
        sprite.moveto(positioned(sprite.rect, center=rightside.center), steps)

        save = self.subscene.readlinesprite.readline.history.add

        save("steps = 60")
        save("sprite.rect.center = rightside.center")
        save("sprite.moveto(positioned(sprite.rect, midright=rightside.midright), steps)")
        save("sprite.moveto(positioned(sprite.rect, topright=rightside.topright), steps)")
        save("sprite.moveto(positioned(sprite.rect, topleft=rightside.topleft), steps)")
        save("sprite.moveto(positioned(sprite.rect, bottomleft=rightside.bottomleft), steps)")
        save("sprite.moveto(positioned(sprite.rect, bottomright=rightside.bottomright), steps)")
        save("sprite.moveto(positioned(sprite.rect, center=rightside.center), steps)")

    def draw(self, surface):
        super().draw(surface)
        self.subscene.draw(surface)

    def update(self):
        super().update()
        self.subscene.update()


def movingsprites():
    screen = screens.desktop_aligned_center((1800,600))
    engine = Engine(screen)
    engine.run(MovingSpriteScene())

def main():
    """
    Working out how to make sprites move on paths with tweens.
    """
    import argparse
    parser = argparse.ArgumentParser(description=main.__doc__)
    args = parser.parse_args()
    movingsprites()

if __name__ == "__main__":
    main()
