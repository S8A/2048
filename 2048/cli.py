import sys
from .board import GameBoard


def main(size, win):
    game = GameBoard(size, win)
    shifts = {'l': game.shift_left,
              'r': game.shift_right,
              'u': game.shift_up,
              'd': game.shift_down,
              'exit': None}
    stop = False
    while not stop:
        print_gameboard(game)
        if game.won():
            print('You won!')
            stop = True
        elif game.lost():
            print('You lost. Try again.')
            stop = True
        else:
            shift = input_shift(shifts)
            if not shift:
                stop = True
            else:
                shift()
            print()


def print_gameboard(gb: GameBoard):
    print(f'..:: {gb.win} GAME ::..')
    print(f'Score: {format_score(gb.score)}')
    print(f'Moves: {gb.moves}')
    print()
    print('+'.join(['-'*6 for i in range(4)]))
    for row in gb.board:
        items = []
        for cell in row:
            if cell == 0:
                items.append(' '*6)
            else:
                items.append(f' {cell :<4} ')
        print('|'.join(items))
        print('+'.join(['-'*6 for i in range(4)]))
    print()


def input_shift(shifts):
    while True:
        user_input = input('Shift board (l/r/u/d): ').strip().lower()
        if user_input in shifts.keys():
            return shifts[user_input]
        else:
            print('ERROR: Invalid shift. Try again.')


def format_score(score):
    if score >= 10**6:
        return f'{round(score / 10**6, 1)}M pts'
    elif score >= 10**3:
        return f'{round(score / 10**3, 1)}k pts'
    else:
        return f'{score} pts'
