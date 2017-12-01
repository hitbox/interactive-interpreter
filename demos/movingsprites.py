import pygame as pg

from interpreter import screens
from interpreter.engine import Engine
from interpreter.globals import g
from interpreter.reloader import run_with_reloader
from interpreter.scenes import BaseScene, ReadlineScene
from interpreter.sprites import FramesPerSecondSprite, Sprite
from interpreter.utils import positioned

from .staging.sprites import MovingSprite, colorsquare, huestrip, saturationvalue, Crosshair

class MovingSpriteScene(BaseScene):

    def __init__(self):
        super().__init__()

        leftside = g.screen.rect.copy()
        leftside.width /= 2

        rightside = g.screen.rect.copy()
        rightside.width /= 2
        rightside.topright = g.screen.rect.topright

        self.rightside = rightside

        pg.draw.rect(g.screen.background,(90,90,90),leftside,1)
        pg.draw.rect(g.screen.background,(90,90,90),rightside,1)

        sprite = MovingSprite()
        sprite.image = pg.Surface((100, 50))
        sprite.image.fill((200,100,100))
        sprite.rect = sprite.image.get_rect()
        self.add(sprite)

        fps = FramesPerSecondSprite()
        fps.rect.topright = (leftside.right - 10, leftside.top + 10)
        self.add(fps)

        steps = 60

        context = dict(g=g, pg=pg, sprite=sprite, s=sprite, positioned=positioned,
                       leftside=leftside, rightside=rightside, steps=steps,
                       self=self, MovingSprite=MovingSprite, fps=fps)

        banner = ReadlineScene.banner + "\nUp/down for example commands to move the sprite on the right."
        self.subscene = ReadlineScene(leftside.inflate(-100, -100), context, banner=banner)
        pg.draw.rect(g.screen.background,(90,200,90),self.subscene.inside,1)

        #g.screen.background.blit(colorsquare(rightside.size), rightside)

        hrect = rightside.copy()
        hrect.height = 100
        hrect.center = rightside.center
        g.screen.background.blit(huestrip(hrect), hrect)

        self.pickerrect = self.rightside.copy()
        self.pickerrect.size = (250, 250)
        self.pickerrect.bottomright = rightside.bottomright

        self.hueimages = {}
        self.hueloaders = {}
        for hue in range(361):
            image = pg.Surface(self.pickerrect.size)
            self.hueimages[hue] = image
            self.hueloaders[hue] = saturationvalue(image, hue)

        self.done = set()

        self.crosshair = Crosshair((100, 100))
        self.crosshair.rect.center = rightside.center
        self.add(self.crosshair)

        self.dirty = True

        sprite.rect.center = rightside.center

        sprite.movetos([positioned(sprite.rect, midright=rightside.midright),
                        positioned(sprite.rect, topright=rightside.topright),
                        positioned(sprite.rect, topleft=rightside.topleft),
                        positioned(sprite.rect, bottomleft=rightside.bottomleft),
                        positioned(sprite.rect, bottomright=rightside.bottomright),
                        positioned(sprite.rect, center=rightside.center)], steps)

        save = self.subscene.readlinesprite.readline.history.add

        save("steps = 60")
        save("sprite.rect.center = rightside.center")
        save("sprite.moveto(positioned(sprite.rect, midright=rightside.midright), steps)")
        save("sprite.moveto(positioned(sprite.rect, topright=rightside.topright), steps)")
        save("sprite.moveto(positioned(sprite.rect, topleft=rightside.topleft), steps)")
        save("sprite.moveto(positioned(sprite.rect, bottomleft=rightside.bottomleft), steps)")
        save("sprite.moveto(positioned(sprite.rect, bottomright=rightside.bottomright), steps)")
        save("sprite.moveto(positioned(sprite.rect, center=rightside.center), steps)")

    def load_iterator(self):
        h, s, v, a = self.color.hsva

        loader = self.hueloaders[h]
        try:
            next(loader)
        except StopIteration:
            self.done.add(h)

    def draw_color_picker(self):
        h, s, v, a = self.color.hsva
        g.screen.background.blit(self.hueimages[h], self.pickerrect)
        self.dirty = False

    def draw(self, surface):
        super().draw(surface)
        self.subscene.draw(surface)
        if self.dirty:
            self.draw_color_picker()

    def update(self):
        super().update()

        self.subscene.update()
        self.color = g.screen.background.get_at(self.crosshair.rect.center)

        self.load_iterator()

        pressed = pg.key.get_pressed()

        speed = 1
        if pressed[pg.K_LEFT]:
            self.crosshair.rect.move_ip(-speed, 0)
            self.dirty = True
        elif pressed[pg.K_RIGHT]:
            self.dirty = True
            self.crosshair.rect.move_ip(speed, 0)


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
    parser.add_argument("--reload", action="store_true",
                        help="Automatically reload if files change.")
    args = parser.parse_args()

    import logging
    logging.basicConfig(level=logging.INFO)

    if args.reload:
        run_with_reloader(movingsprites())
    else:
        movingsprites()

if __name__ == "__main__":
    main()
