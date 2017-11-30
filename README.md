# Python 3

## pygame interactive interpreter

Another attempt of mine to make an interactive interpreter usable in pygame.

## demo

`python -m demos.interpreter`

## side-by-side interpreter demo

`python demos.movingsprites`

## Status

Development

## Features

* textwrapping (on characters)
* closely emulating `code.InteractiveConsole`
* simple readline class with history

## TODO

* readline scene needs serious cleanup and the idea of a scene is probably a dead end.

* `ReadlineScene` moved to an "object" that can put anywhere (or a general reorganizing and cleanup)
* clear screen (like CTRL+l)
* toggle console (like Kuake for KDE)
* syntax highlighting
* only one input control should receive key events
* engine shutdown event
* add a pager?

## NOTES

* `debugging` dir includes things used to work out a problem. They may not work.
