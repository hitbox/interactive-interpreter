import pygame as pg

def border(image, color=(255,255,255), thickness=1):
    pg.draw.rect(image, color, image.get_rect(), thickness)
    return image
