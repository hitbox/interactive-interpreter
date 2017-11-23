import pygame as pg

DEFAULT_COLOR = (255,255,255)
DEFAULT_THICKNESS = 1

def border(image, color=DEFAULT_COLOR, thickness=DEFAULT_THICKNESS):
    pg.draw.rect(image, color, image.get_rect(), thickness)
    return image

def borderright(image, color=DEFAULT_COLOR, thickness=DEFAULT_THICKNESS):
    rect = image.get_rect()
    pg.draw.rect(image, color, pg.Rect(rect.right - thickness, rect.top, thickness, rect.height))
    return image
