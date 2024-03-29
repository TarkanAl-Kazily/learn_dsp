# Copyright 2023 Tarkan Al-Kazily 

import wave
import numpy as np

from common.effect import Effect
from common.utils import read_from_wav

_sample_rate = 44100

_BLOCK_SIZE = 2 ** 12

def prepare_wav_file(f):
    global _sample_rate
    f.setframerate(_sample_rate)
    f.setnchannels(1)
    f.setsampwidth(2)

class Distortion(Effect):
    """
    Applies distortion through amplifying the audio (with clipping)

    Attributes:
    - volume: Amplification factor (float) - 1.0 representing no amp, 2.0 doubling volume
    """

    def __init__(self, volume, **kwargs):
        self.volume = volume
        super().__init__(**kwargs)

    def process_mono(self, audio):
        return np.multiply(self.volume, audio).astype(np.int16)

def main(args):
    global _sample_rate
    print(f"Applying a distortion effect to {args.output_audio} with volume {args.volume}")

    _sample_rate = args.sample_rate
    effect = Distortion(volume = args.volume, sample_rate = _sample_rate)

    with wave.open(args.input_audio, 'rb') as inf, wave.open(args.output_audio, 'wb') as outf:
        # Check that sample rate matches expected rate
        if inf.getframerate() != _sample_rate:
            raise Exception(f"Input audio has a sample rate of {inf.getframerate()}, expected {_sample_rate}")

        nchannels, sampwidth, framrate, nframes, _, _ = inf.getparams()
        print(f"Processing {args.input_audio}: ch {nchannels}, width {sampwidth} rate {framrate} samples {nframes}")

        prepare_wav_file(outf)
        for i in range(0, inf.getnframes(), _BLOCK_SIZE):
            block = read_from_wav(inf, _BLOCK_SIZE, mono=(nchannels == 1))
            outf.writeframes(effect.process_mono(block))
