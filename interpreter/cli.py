import argparse

import pygame as pg

from . import window
from .engine import Engine
from .rect import Rect
from .scenes import ReadlineScene, TextSpriteScene
from .screens import Screen
from .sprites import RectSprite

def tuplelizer(s):
    return tuple(map(int, s.split('x')))

def main():
    """
    Start an interactive python interpreter, in a pygame GUI.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    scenemap = {
        'readline': ReadlineScene,
        'textsprite': TextSpriteScene,
    }
    parser.add_argument(
        '--scene',
        choices = list(scenemap),
        default = 'readline',
        help = 'The scene to run. Default: %(default)s'
    )
    parser.add_argument(
        '--size',
        type = tuplelizer,
        default = "1000x900",
        help = 'Window size. Default: %(default)s'
    )
    parser.add_argument(
        '--align',
        choices = ['topleft', 'midtop', 'topright', 'midright', 'bottomright',
                   'midbottom', 'bottomleft', 'midleft'],
        default = 'midright',
        help='Align window to desktop. Default: %(default)s'
    )
    args = parser.parse_args()

    # set window aligned midright to desktop
    desktop_rect = window.get_desktop_rect().get_rect()

    window_rect = Rect(args.size).get_rect(midright = (desktop_rect.right - 10, desktop_rect.centery))

    window.set_position(window_rect.topleft)

    display = Screen(window_rect.size)

    e = Engine(display)

    inside = RectSprite((800, 800))
    inside.move_ip(50, 50)

    scene_class = scenemap[args.scene]

    e.run(scene_class(inside))
