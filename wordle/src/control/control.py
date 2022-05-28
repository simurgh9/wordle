"""
Author: Tashfeen, Ahmad

The MIT License (MIT)
"""

from wordle.src.model.model import Model
from wordle.src.model.constant import ALLOWED, CHEAT


class Control:
    def __init__(self, M):
        self.M = M

    def handle(self, key):
        key = self.parse_key(key)
        if key == 'KEY_ESCAPE':
            return False
        if key == ' ' or self.model().state()['gameover']:
            self.M = Model(stats=self.model().stats)
        elif key in CHEAT:
            self.model().write(color=int(key))
        elif key == '\'':
            self.model().check(recolor=False)
        elif key == 'KEY_TAB':
            self.model().toggle_player_info()
        elif key == 'KEY_ENTER':
            self.model().check()
        elif key == 'KEY_BACKSPACE':
            self.model().backspace()
        elif key:
            self.model().write(key=key)
        return True

    def parse_key(self, key):
        k = key.name if key.is_sequence else str(key)
        return k if k in ALLOWED else False

    def model(self):
        return self.M
