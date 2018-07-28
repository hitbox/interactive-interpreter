import pygame as pg

def top2bottom(images):
    """
    Join images from top to bottom.

    :param images: iterable of images.
    :type images: iter
    """
    rects = [image.get_rect() for image in images]

    final_rect = pg.Rect(0, 0, max(rect.width for rect in rects), sum(rect.height for rect in rects))
    final_image = pg.Surface(final_rect.size, pg.SRCALPHA)

    y = 0
    for rect, image in zip(rects, images):
        final_image.blit(image, (0, y))
        y += rect.height

    return final_image
