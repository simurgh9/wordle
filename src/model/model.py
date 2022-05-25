"""
Author: Tashfeen, Ahmad

The MIT License (MIT)
"""

from src.model.constant import YELLOW, GREEN, COLS, ROWS, PL
from src.model.constant import LOSER, PLAYING, WINNER, MESSAGE
from src.model.constant import FILENAME, STATS
from random import choice


class Model:
    def __init__(self, stats=None):
        self.sieved = self.__word_list__()
        self.LIST = set(self.sieved)
        self.WORD = choice(self.sieved)
        self.status = PLAYING
        self.stats = stats if stats else STATS
        self.print_player_info = False
        self.cursor, self.board = [0, 0], []
        self.board = [[list(PL) for c in range(COLS)] for r in range(ROWS)]
        self.__set_message__(MESSAGE)

    def state(self):
        return {
            'board': self.board,
            'message': self.message,
            'sieved': self.sieved,
            'stats': self.stats,
            'gameover': self.status != PLAYING,
            'print_player_info': self.print_player_info,
        }

    def toggle_player_info(self):
        self.print_player_info = not self.print_player_info

    def check(self, recolor=True):
        if self.cursor[0] < ROWS and self.cursor[1] == COLS:
            self.__set_message__('Not in wordlist.')
            if self.__current_word__() in self.LIST:
                if recolor:
                    self.__recolor__()
                self.__sieve_list__()
                self.__set_message__('Hmmm...')
                self.status = self.__eval_status__()
                self.update_stats()
                if self.status > PLAYING:
                    self.__set_message__(f'Winner! {MESSAGE}')
                elif self.status < PLAYING:
                    self.__set_message__(f'Loser! {MESSAGE}')
                self.cursor = [self.cursor[0] + 1, 0]

    def update_stats(self):
        if not self.state()['gameover']:
            return
        self.stats['played'] += 1
        if self.status == WINNER:
            self.stats['won'] += 1
            self.stats['distribution'][self.cursor[0]] += 1

    def backspace(self):
        if self.cursor[1] > 0:
            self.cursor[1] -= 1
            i, j = self.cursor
            self.board[i][j] = list(PL)

    def write(self, key=None, color=None):
        if self.cursor[0] < ROWS and self.cursor[1] < COLS:
            i, j = self.cursor
            if color is not None:
                self.board[i][j][1] = color
                return
            self.board[i][j][0] = key
            self.cursor[1] += 1

    def __current_word__(self, color=False, both=False):
        if both:
            return [c for c in list(self.board[self.cursor[0]])]
        if color:
            return [c[1] for c in list(self.board[self.cursor[0]])]
        return ''.join([c[0] for c in list(self.board[self.cursor[0]])])

    def __recolor__(self):
        new_colors = self.__color__(self.__current_word__(), self.WORD)
        for cell, color in zip(self.board[self.cursor[0]], new_colors):
            cell[1] = color

    def __color__(self, word, target):
        colors = [PL[1] for c in word]
        freq, greens = {c: target.count(c) for c in target}, []
        for i in range(COLS):
            if word[i] == target[i]:
                colors[i] = GREEN
                freq[word[i]] -= 1
                greens.append(i)
        for i in range(COLS):
            if i in greens:
                continue
            if freq.get(word[i], 0) <= 0:
                continue
            if word[i] in target:
                colors[i] = YELLOW
                freq[word[i]] -= 1
        return colors

    def __sieve_list__(self):
        word, sieved = self.__current_word__(both=True), self.sieved
        known = [c[0] for c in word if (c[1] == GREEN) or (c[1] == YELLOW)]
        freq = {c: known.count(c) for c in known}
        for i in range(COLS):
            ltr, clr = word[i]
            if clr == PL[1]:
                self.__purge__(lambda j: ltr in sieved[j] and
                               sieved[j].count(ltr) > freq.get(ltr, 0))
            elif clr == GREEN:
                self.__purge__(lambda j: ltr != sieved[j][i])
            elif clr == YELLOW:
                self.__purge__(lambda j: ltr == sieved[j][i])
            if ltr in freq:
                self.__purge__(lambda j: sieved[j].count(ltr) < freq[ltr])

    def __purge__(self, to_be_deleted):
        j = 0
        while j < len(self.sieved):
            if to_be_deleted(j):
                del self.sieved[j]
                continue
            j += 1

    def __word_list__(self):
        with open(FILENAME, 'r') as fl:
            words = [ln.strip().split(',') for ln in fl.readlines()]
            words = [(word[0], float(word[1])) for word in words]
            words = sorted(words, key=lambda x: x[1], reverse=True)
            words = [word[0] for word in words]
        return words

    def __set_message__(self, message):
        self.message = message

    def __eval_status__(self):
        if self.__current_word__(True) == [GREEN for i in range(COLS)]:
            return WINNER
        if self.cursor[0] >= ROWS - 1:
            return LOSER
        return PLAYING
