"""
Author: Tashfeen, Ahmad

The MIT License (MIT)
"""

from src.model.model import Model
from src.view.view import View
from src.control.control import Control
from src.control.player import Human, Dolittle, Scribe
from argparse import ArgumentParser


parser = ArgumentParser(
    prog='wordle',
    description='A word-game by Josh Wardle--implementation by Tashfeen.')
parser.add_argument('--scribe', '-s', nargs=2, metavar=('opener', 'N'),
                    help='Play N games with opener headlessly and log stats.')
parser.add_argument('--dolittle', '-d', action='store_true',
                    help='Have Dolittle play 100 games with "artsy."')
parser.add_argument('--data', '-dt', action='store_true',
                    help='Print out the wordlist CSV data.')

args = parser.parse_args()
view = View(Control(Model()))


def produce_data():
    # Bellow is the javascript source downloaded from
    # the Wordle website on 27 Feb 2022 to extract the
    # words.
    with open('data/main.4d41d2be.js') as fl:
        js = fl.read()
        js = js[js.index('Ma=[')+4:]
        js = js[:js.index(']')]
        words = js.strip().split(',')
        words = [w.strip()[1:-1] for w in words]

    # Bellow is the popular five words data downloaded
    # from Wolfram with their frequencies in English.
    with open('data/words.csv') as fl:
        freq = {}
        for line in fl.readlines():
            line = line.strip().split(',')
            freq[line[0]] = float(line[1])

    # These are words present in the list from
    # data/main.4d41d2be.js but absent from the Wolfram
    # data. I downloaded their frequencies from Wolfram
    # separately.
    with open('data/absent.csv') as fl:
        for line in fl.readlines():
            line = line.strip().split(',')
            freq[line[0]] = float(line[1])

    for word in words:
        print(f'{word},{freq[word]}')


def main():
    if args.data:
        produce_data()
        return
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
