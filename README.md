# Python 3

## pygame interactive interpreter

Another attempt of mine to make an interactive interpreter usable in pygame.

## Status

Development

## Features

* textwrapping (on characters)
* closely emulating `code.InteractiveConsole`
* simple readline class with history

## TODO

* get moving sprites working and...
* fix interpreter scene to work with simpler engine event dispatcher (broke it with debugging/moving_sprites.py)

* `ReadlineScene` moved to an "object" that can put anywhere (or a general reorganizing and cleanup)
* clear screen
* toggle console (like Kuake for KDE)
* syntax highlighting
* only one input control should recieve key events
* engine shutdown event
