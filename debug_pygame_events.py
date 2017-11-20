import argparse
import pygame as pg

def run(only=None):
    pg.display.init()
    pg.display.set_mode((320, 340))

    running = True
    while running:
        for event in pg.event.get():
            if not only or (only and event.type in only):
                print(event)
            if event.type == pg.QUIT:
                running = False
        pg.display.flip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="+", help="Print only events of this type(s).")
    args = parser.parse_args()

    only_types = [getattr(pg, name) for name in args.only]

    run(only=only_types)

if __name__ == "__main__":
    main()
