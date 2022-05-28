"""
Author: Tashfeen, Ahmad

The MIT License (MIT)
"""

from time import sleep
from blessed import Terminal
from wordle.src.model.constant import COLS
from abc import ABC, abstractmethod
from blessed.keyboard import Keystroke


class Player(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def moves(self):
        pass

    def model_state(self):
        return self.game.control().model().state()

    def print_info(self):
        sieved = self.model_state()['sieved']
        length = COLS + (2*self.game.PADDING_LEN) + self.game.PADDING_LEN
        p = self.game.padding()
        rows = int(0.45*self.game.term.height)
        cols = self.game.term.width // length
        for i in range(rows):
            row = sieved[i*cols: i*cols+cols]
            fmt_str = ''.join([p + '{}' + p for i in row])
            self.game.print_centered(fmt_str.format(*row))


class Human(Player):
    def moves(self):
        term = Terminal()
        with term.cbreak():
            while True:
                yield term.inkey()


class Dolittle(Player):
    def __init__(self, game, opener, maximum):
        super().__init__(game)
        self.OPENER = opener
        self.N = maximum
        self.n = 0

    def print_info(self):
        stats = self.model_state()['stats']
        won = int(stats["won"])
        total = int(stats["played"])
        dist = stats["distribution"]
        if total > 0:
            dist = [n/total for n in dist]
            won = won/total
        dist = '  '.join([f'{p:.2f}' for p in dist])
        to_print = f'{self.n:<6}{won:.2f} with {dist}'
        self.game.print_centered(to_print)

    def moves(self):
        while self.n < self.N:
            i = 0
            yield Keystroke(ucs='KEY_TAB')  # turn on player info
            while not self.model_state()['gameover']:
                most_probable = self.model_state()['sieved'][0]
                word = self.OPENER if i == 0 else most_probable
                for letter in word:
                    sleep(0.2)
                    yield Keystroke(ucs=letter)
                sleep(0.5)
                yield Keystroke(ucs='KEY_ENTER')
                i += 1
            sleep(0.5)
            yield Keystroke(ucs=' ')
            self.n += 1
        yield Keystroke(ucs='KEY_ESCAPE')


class Scribe(Dolittle):
    def __init__(self, game, opener, maximum):
        super().__init__(game, opener, maximum)
        game.headless = True
        game.clear_on_exit = False

    def moves(self):
        while self.n < self.N:
            i = 0
            yield Keystroke(ucs='KEY_TAB')  # turn on player info
            while not self.model_state()['gameover']:
                most_probable = self.model_state()['sieved'][0]
                word = self.OPENER if i == 0 else most_probable
                for letter in word:
                    yield Keystroke(ucs=letter)
                yield Keystroke(ucs='KEY_ENTER')
                i += 1
            yield Keystroke(ucs=' ')
            self.n += 1
        yield Keystroke(ucs='KEY_ESCAPE')
