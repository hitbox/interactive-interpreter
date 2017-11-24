import argparse
import inspect
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame as pg

import interpreter.font
import interpreter.window

interpreter.window.centered()

def _wrapper(font, inside, text):
    char_rects = []
    last = None
    for char in text:
        rect = pg.Rect((0,0),font.size(char))
        if last is None:
            rect.topleft = inside.topleft
        else:
            rect.bottomleft = last.bottomright
            if rect.right > inside.right:
                rect.topleft = (inside.left, last.bottom)
        last = rect
        if char == "\n":
            rect.topleft = (inside.left, last.bottom)
        if rect.bottom > inside.bottom:
            break
        char_rects.append(rect)
    return char_rects

def wrapper(font, inside, text, _cache={}):
    key = (font, tuple(inside), text)
    if key not in _cache:
        _cache[key] = _wrapper(font, inside, text)
    return _cache[key]

class Drag:

    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
        self.dragging = False


def run():
    pg.display.init()
    SIZE = (900, 800)
    screen = pg.display.set_mode(SIZE)
    world = screen.get_rect()
    background = screen.copy()

    description = ("Simple text wrapping\n"
                   "with pygame Font\n\n"
                   "Drag lower-right corner.\n"
                   "Escape, q: to quit\n"
                   "r: toggle char rects\n"
                   "a: increase font size\n"
                   "z: decrease font size\n"
                   "d: toggle draw with Font\n"
                   "   class or manually\n")
    image = interpreter.font.Font(color=(125,125,125), fontsize=48).render(description)
    background.blit(image, image.get_rect(topright=world.topright))

    font = interpreter.font.Font()
    text = inspect.getsource(sys.modules[__name__])
    inside = screen.get_rect()
    inside.topleft = (world.left + 25, world.top + 25)
    inside.size = (200, 600)

    drag = Drag(inside.copy(), (75,75,75))
    drag.rect.size = (25, 25)
    drag.rect.bottomright = inside.bottomright

    draw_char_rects = False
    draw_old_style = False

    font_speed = 4

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_q, pg.K_ESCAPE):
                    pg.event.post(pg.event.Event(pg.QUIT))
                elif event.key == pg.K_r:
                    draw_char_rects = not draw_char_rects
                elif event.key == pg.K_a:
                    font.fontsize += font_speed
                elif event.key == pg.K_z:
                    font.fontsize -= font_speed
                elif event.key == pg.K_d:
                    draw_old_style = not draw_old_style
                    if draw_old_style:
                        print("Drawing manually")
                    else:
                        print("Drawing with Font class")
            elif event.type == pg.MOUSEMOTION:
                if drag.dragging:
                    drag.rect.move_ip(event.rel)
                elif drag.rect.collidepoint(event.pos):
                    drag.color = (200,200,200)
                else:
                    drag.color = (75,75,75)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if drag.rect.collidepoint(event.pos):
                    drag.dragging = True
            elif event.type == pg.MOUSEBUTTONUP:
                drag.dragging = False

        if drag.dragging:
            inside.width = drag.rect.right - inside.left
            inside.height = drag.rect.bottom - inside.top

        screen.blit(background, (0,0))

        pg.draw.rect(screen, drag.color, inside, 1)
        pg.draw.rect(screen, drag.color, drag.rect, 1)

        if draw_old_style:
            rects = wrapper(font, inside, text)
            for char, rect in zip(text, rects):
                image = font.render(char)
                screen.blit(image, rect)
                if draw_char_rects:
                    pg.draw.rect(screen, (25,255,25), rect, 1)
        else:
            image = font.render(text, inside)
            screen.blit(image, inside)

        pg.display.flip()

def main():
    """
    Created to work out how to wrap text.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    args = parser.parse_args()

    run()

if __name__ == "__main__":
    main()
