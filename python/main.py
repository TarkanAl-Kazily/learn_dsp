import argparse

import basic_oscillator
import basic_signals
import delay
import distortion
import reverb

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

    signals = subparsers.add_parser("basic_signals", help="Generate basic signals")
    signals.add_argument('filename')
    signals.add_argument('-t', '--signal-type', choices=[1, 2, 3, 4, 5], type=int)
    signals.set_defaults(func=basic_signals.main)

    dist = subparsers.add_parser("distortion", help="Apply distortion")
    dist.add_argument('input_audio')
    dist.add_argument('output_audio')
    dist.add_argument('-v', '--volume', default=2.0, type=float)
    dist.set_defaults(func=distortion.main)

    rvb = subparsers.add_parser("reverb", help="Apply reverb")
    rvb.add_argument('input_audio')
    rvb.add_argument('output_audio')
    rvb.add_argument('--test', action="store_true")
    rvb.set_defaults(func=reverb.main)

    dly = subparsers.add_parser("delay", help="Apply delay")
    dly.add_argument('input_audio')
    dly.add_argument('output_audio')
    dly.add_argument('--time', default=0.1, type=float, help="Delay time seconds")
    dly.add_argument('--feedback', default=0.3, type=float, help="Delay feedback")
    dly.add_argument('--mix', default=0.5, type=float, help="Delay mix - 0 is Dry")
    dly.set_defaults(func=delay.main)

    return parser.parse_args()

def main(args):
    args.func(args)

if __name__ == "__main__":
    main(parse())
