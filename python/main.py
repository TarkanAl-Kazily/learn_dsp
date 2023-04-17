import argparse

import basic_oscillator

WAVS = "../wavs/"

def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename')
    parser.add_argument('-d', '--dir', default=WAVS)

    parser.add_argument('-f', '--frequency', default=440.0, type=float)

    parser.add_argument('--sample-rate', default=44100, type=int)

    return parser.parse_args()

def main(args):
    basic_oscillator.main(args)

if __name__ == "__main__":
    main(parse())
