def interpreterdemo():
    import pygame as pg

    from interpreter import screens
    from interpreter.engine import Engine
    from interpreter.globals import g
    from interpreter.scenes import ReadlineScene

    screen = screens.desktop_aligned_midright((1000,900))
    screen.background.fill((31,31,31))
    engine = Engine(screen)
    banner = ReadlineScene.banner + "\nDemonstration of a console in pygame."
    scene = ReadlineScene(g.screen.rect.inflate(-25, -25),
                          dict(g=g, pg=pg),
                          banner=banner)
    engine.run(scene)

def main():
    """
    Interactive Interpreter in Pygame.
    """
    import argparse
    parser = argparse.ArgumentParser(description=main.__doc__)
    args = parser.parse_args()

    interpreterdemo()

if __name__ == "__main__":
    main()
