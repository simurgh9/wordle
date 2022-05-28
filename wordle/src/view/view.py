"""
Author: Tashfeen, Ahmad

The MIT License (MIT)
"""

from math import ceil
from traceback import print_exc
from blessed import Terminal
from signal import signal, SIGWINCH
from wordle.src.model.constant import GREY, YELLOW, GREEN, COLS


class View:
    def __init__(self, C, player=None, headless=False):
        self.C, self.player, self.headless = C, player, headless
        self.PADDING_LEN = 1
        self.PADDING_CHR = ' '
        self.clear_on_exit = True
        self.term = Terminal()
        self.PALETTE = [-1, -1, -1]
        self.PALETTE[GREY] = self.term.white_on_black
        self.PALETTE[YELLOW] = self.term.white_on_yellow
        self.PALETTE[GREEN] = self.term.white_on_green
        signal(SIGWINCH, self.on_resize)

    def on_resize(self, *args):
        self.paint()

    def event_loop(self):
        try:
            self.paint()
            for move in self.player.moves():
                if not self.control().handle(move):
                    break
                self.paint()
        except BaseException:
            self.clear()
            self.clear_on_exit = False
            if input('Unexpected halt. Print backtrace? <y/n> ') == 'y':
                print_exc()
        if self.clear_on_exit:
            self.clear()

    def paint(self):
        if not self.headless:
            self.print_model()
        if self.control().model().state()['print_player_info']:
            self.player.print_info()
        if not self.headless:
            self.position_cursor()

    def print_model(self):
        self.clear()
        state = self.control().model().state()
        self.print_centered(state["message"] + '\n')
        for line in state['board']:
            p = self.padding()
            colored = [self.PALETTE[c[1]](p + c[0].upper() + p) for c in line]
            self.print_centered(''.join(colored))
        print()

    def position_cursor(self):
        width = COLS*(2*self.PADDING_LEN+1)
        cursor = [i for i in self.control().model().cursor]
        padding = ceil(self.term.width / 2) - width // 2
        y, x = cursor[0]+2, cursor[1]+padding+(cursor[1]*2*self.PADDING_LEN)
        print(self.term.move_yx(y, x), end='', flush=True)

    def print_centered(self, string):
        if '\n' not in string:
            print(self.term.center(string))
            return
        for sub in string.split('\n'):
            print(self.term.center(sub))

    def clear(self):
        print(self.term.home + self.term.clear, end='', flush=True)

    def control(self):
        return self.C

    def padding(self):
        return self.PADDING_CHR*self.PADDING_LEN
