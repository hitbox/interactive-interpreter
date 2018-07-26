import pygame as pg

def ReadlineEvent(action, value):
    return pg.event.Event(pg.USEREVENT, subtype="readline", action=action, value=value)
