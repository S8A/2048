import argparse
from . import cli, gui


def main(args):
    if args['cli']:
        cli.main(args['size'], args['win'])
    else:
        gui.main(args['size'], args['win'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2048 game.')
    parser.add_argument('size', metavar='N', type=int, nargs='?',
                        default=4, help='NxN will be the size of the board')
    parser.add_argument('win', metavar='W', type=int, nargs='?',
                        default=2048, help='cell number needed to win')
    parser.add_argument('--cli', action='store_true',
                        help='run command-line version of the game')
    args = parser.parse_args()
    main(vars(args))
