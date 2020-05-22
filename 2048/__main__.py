import argparse


def main(args):
    # TODO: Actual game
    print(f'2048 game: {args["n"]}x{args["n"]} board.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2048 game.')
    parser.add_argument('n', metavar='N', type=int, nargs='?',
                        default=4, help='nxn will be the size of the board')
    args = parser.parse_args()
    main(vars(args))
