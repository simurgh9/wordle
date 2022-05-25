"""
Author: Tashfeen, Ahmad

The MIT License (MIT)
"""

FILENAME = 'data/wordle.csv'
GREY, YELLOW, GREEN = 0, 1, 2
PL = ['?', GREY]  # placeholder
COLS, ROWS = 5, 6
LOSER, PLAYING, WINNER = -1, 0, 1
MESSAGE = '[ESC] to end or [SPC] to reset.'
STATS = {'played': 0, 'won': 0, 'distribution': [0 for i in range(ROWS)]}
ALPHABET = [chr(i) for i in range(97, 123)]
MOVEMENT = ['KEY_ENTER', 'KEY_BACKSPACE']
WINDOW = ['\'', ' ', 'KEY_TAB', 'KEY_ESCAPE']
CHEAT = [str(GREY), str(YELLOW), str(GREEN)]
ALLOWED = ALPHABET + MOVEMENT + WINDOW + CHEAT
