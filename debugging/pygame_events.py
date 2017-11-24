import argparse

import pygame as pg

def run(only=None):
    pg.display.init()
    pg.font.init()
    background = pg.display.set_mode((320, 340))
    world = background.get_rect()

    font = pg.font.Font(None, 24)
    image = font.render("Close with window close button.", True, (255,255,255))
    background.blit(image, image.get_rect(center=world.center))
    pg.display.flip()

    running = True
    while running:
        for event in pg.event.get():
            if not only or (only and event.type in only):
                print(event)
            if event.type == pg.QUIT:
                running = False

def main():
    """
    Print the events pygame is posting.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--only", nargs="+",
                        help="Print only events of this pygame type(s). Use the"
                             " upper-case names.")
    args = parser.parse_args()

    if args.only:
        only_types = [getattr(pg, name) for name in args.only]
    else:
        only_types = []

    run(only=only_types)

if __name__ == "__main__":
    main()
