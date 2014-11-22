#!/usr/bin/env python
import os
import sys

if sys.version_info[0] > 2:
    print("This game runs on python 2 only")

#Export current working directory as environment variable for use by modules
#( there's probably a more "python" way to do this... )
#Note: environment variable doesn't persist when chess process closes, so
#this is probably a reasonably OK thing to do
os.environ['KALEKOCHESS_TOP_DIR']=os.path.dirname(os.path.realpath(__file__))
print os.environ['KALEKOCHESS_TOP_DIR']

from chesslib import board

# Load a save if it exists
if os.path.exists("state.fen"):
    with open("state.fen") as save:
        game = board.Board(save.read())
else:
    game = board.Board()

# Choose display method
if len(sys.argv) > 1:
    if sys.argv[1] in ('--console', '-c'):
        from chesslib.gui_console import display
        display(game)
        exit(0)
    elif sys.argv[1] in ('--help', '-h'):
        print '''Usage: game.py [OPTION]\n\n\tPlay a game of chess\n\n\tOptions:\n\t -c, --console\tplay in console mode\n\n'''
        exit(0)

try:
    from chesslib.gui_tkinter import display
except ImportError:
    from chesslib.gui_console import display
finally:
    display(game)
