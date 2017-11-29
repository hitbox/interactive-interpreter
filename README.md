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

* reflow while typing--readline sprite is going outside it's boundaries.
* readline scene needs serious cleanup and the idea of a scene is probably a dead end.

* `ReadlineScene` moved to an "object" that can put anywhere (or a general reorganizing and cleanup)
* clear screen
* toggle console (like Kuake for KDE)
* syntax highlighting
* only one input control should recieve key events
* engine shutdown event
* add a pager?
