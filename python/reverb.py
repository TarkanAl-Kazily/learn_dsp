# Copyright 2023 Tarkan Al-Kazily 

import wave
import numpy as np

from common.effect import Effect
from common.utils import read_from_wav, stereo_to_frames

_sample_rate = 48000

_BLOCK_SIZE = 2 ** 12

def prepare_wav_file(f):
    """
    Sets up file f for the reverb output
    """
    global _sample_rate
    f.setframerate(_sample_rate)
    f.setnchannels(2)
    f.setsampwidth(2)

class Reverb(Effect):
    """
    A Reverb algorithm.
    """

    def __init__(self, sample_rate):
        super().__init__(sample_rate)

    def process_stereo(self, audio):
        pass

class TestStereo(Effect):
    """
    A Reverb algorithm.
    """

    def __init__(self, sample_rate):
        super().__init__(sample_rate)

    def process_stereo(self, audio):
        result = np.stack((audio, audio), axis=-1)
        return result

def main(args):
    global _sample_rate
    print(f"Applying a reverb effect to {args.output_audio}")

    _sample_rate = args.sample_rate
    effect = Reverb(sample_rate = _sample_rate)

    if args.test:
        effect = TestStereo(sample_rate = _sample_rate)

    with wave.open(args.input_audio, 'rb') as inf, wave.open(args.output_audio, 'wb') as outf:
        # Check that sample rate matches expected rate
        if inf.getframerate() != _sample_rate:
            raise Exception(f"Input audio has a sample rate of {inf.getframerate()}, expected {_sample_rate}")

        nchannels, sampwidth, framrate, nframes, _, _ = inf.getparams()
        print(f"Processing {args.input_audio}: ch {nchannels}, width {sampwidth} rate {framrate} samples {nframes}")

        prepare_wav_file(outf)

        for i in range(0, inf.getnframes(), _BLOCK_SIZE):
            block = read_from_wav(inf, _BLOCK_SIZE, mono=(nchannels == 1))
            stereo_data = effect.process_stereo(block)
            outf.writeframes(stereo_to_frames(stereo_data))
