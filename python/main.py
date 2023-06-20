import argparse

import basic_oscillator
import distortion

WAVS = "../wavs/"

def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('--sample-rate', default=44100, type=int)
    parser.add_argument('-d', '--dir', default=WAVS)
    subparsers = parser.add_subparsers(help="Modes", required=True)

    bosc = subparsers.add_parser("basic_oscillator", help="Generate basic waves")
    bosc.add_argument('filename')
    bosc.add_argument('-f', '--frequency', default=440.0, type=float)
    bosc.set_defaults(func=basic_oscillator.main)

    dist = subparsers.add_parser("distortion", help="Apply distortion")
    dist.add_argument('input_audio')
    dist.add_argument('output_audio')
    dist.add_argument('-v', '--volume', default=2.0, type=float)
    dist.set_defaults(func=distortion.main)

    return parser.parse_args()

def main(args):
    args.func(args)

if __name__ == "__main__":
    main(parse())
