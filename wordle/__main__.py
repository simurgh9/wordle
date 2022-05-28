"""
Author: Tashfeen, Ahmad

The MIT License (MIT)
"""

from argparse import ArgumentParser
from wordle.src.view.view import View
from wordle.src.model.model import Model
from wordle.src.control.control import Control
from wordle.src.control.player import Human, Dolittle, Scribe


parser = ArgumentParser(
    prog='wordle',
    description='A word-game by Josh Wardle--implementation by Tashfeen.')
parser.add_argument('--scribe', '-s', nargs=2, metavar=('opener', 'N'),
                    help='Play N games with opener headlessly and log stats.')
parser.add_argument('--dolittle', '-d', action='store_true',
                    help='Have Dolittle play 100 games with "artsy."')

args = parser.parse_args()
view = View(Control(Model()))


def main():
    if args.dolittle:
        view.player = Dolittle(view, 'artsy', 100)
    elif args.scribe:
        valid = args.scribe[0] in view.control().model().LIST
        is_unsigned_int = args.scribe[1].isdigit()
        if not valid:
            print(f'{args.scribe[0]} is not a valid Wordle word.')
        if not is_unsigned_int:
            print(f'{args.scribe[1]} is not a valid unsigned integer.')
        if valid and is_unsigned_int:
            view.player = Scribe(view, args.scribe[0], int(args.scribe[1]))
    view.player = Human(view) if view.player is None else view.player
    view.event_loop()


if __name__ == '__main__':
    main()
