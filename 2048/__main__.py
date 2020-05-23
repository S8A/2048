import argparse


def main(args):
    # TODO: Actual game
    print(f'{args["win"]} game: {args["size"]}x{args["size"]} board.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2048 game.')
    parser.add_argument('size', metavar='N', type=int, nargs='?',
                        default=4, help='NxN will be the size of the board')
    parser.add_argument('win', metavar='W', type=int, nargs='?',
                        default=2048, help='cell number needed to win')
    args = parser.parse_args()
    main(vars(args))
