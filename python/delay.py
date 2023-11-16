# Copyright 2023 Tarkan Al-Kazily 

import wave
import numpy as np

from common.effect import Effect
from common.utils import read_from_wav, stereo_to_frames

_sample_rate = 48000

_BLOCK_SIZE = 2 ** 10

def prepare_wav_file(f):
    """
    Sets up file f for the reverb output
    """
    global _sample_rate
    f.setframerate(_sample_rate)
    f.setnchannels(1)
    f.setsampwidth(2)

class MonoDelay(Effect):
    """
    A baseic Delay algorithm.

    Attributes:
    - time: The time in seconds to delay the audio
    - feedback: The level of feedback to apply (0 to 1)
    - mix: The level of mixing between the delayed audio and dry audio
        0.0 -> Dry audio entirely
        1.0 -> Wet audio entirely
    """

    def __init__(self, sample_rate, time, feedback, mix, state_size_s=5):
        """
        Arguments:
        - sample_rate
        - time
        - feedback
        - mix
        - state_size_s: Configures the maximum size of the delay line buffer internal state
        """
        super().__init__(sample_rate)

        if time > state_size_s:
            raise Exception(f"Maximum delay line buffer size {state_size_s} (s) is smaller than the delay time {time} (s)")

        self.time = time
        self.feedback = feedback
        self.mix = mix

        # Internal attributes
        self._state = np.zeros((state_size_s * sample_rate), dtype=np.int16)
        self._delay_samples = int(time * sample_rate)
        self._delay_start = 0

        if self._delay_samples < _BLOCK_SIZE:
            raise Exception(f"Delay line buffer size {state_size_s} (s) is smaller than the block size")

    def process_mono(self, audio):
        """
        Input signals:
            * audio (dry signal)
            * state (delay line after applying buffering and feedback gain)

        Output signals:
            * new state (incorporating buffering and feedback gain)
            * mixed signal
        """
        samples = audio.shape[0]
        # 1. Sum current state with output audio according to mix level
        #    State buffer is delay time seconds samples long, and loops. This means that a given
        #    impulse signal is only re-added to the output after the delay time passes.
        output = audio * (1.0 - self.mix)
        # Splice arrays
        # [self._delay_start -> min( end, self._delay_start + audio.shape[0])]
        # [0 -> audio.shape[0] - (end - self._delay_start)]
        trailing_fdb_samples = min(self._delay_samples, self._delay_start + samples) - self._delay_start
        leading_fdb_samples = samples - trailing_fdb_samples
        assert trailing_fdb_samples + leading_fdb_samples == samples, f"{trailing_fdb_samples} + {leading_fdb_samples} != {samples}"

        if leading_fdb_samples == 0:
            output += self._state[self._delay_start:self._delay_start + trailing_fdb_samples] * self.mix
        else:
            output[:trailing_fdb_samples] += self._state[self._delay_start:self._delay_start + trailing_fdb_samples] * self.mix
            output[trailing_fdb_samples:] += self._state[0:leading_fdb_samples] * self.mix

        # Note: this assumes a minimum delay size that's greater than the block size

        # 2. Update state with the same output & 
        # 3. Apply feedback to updated samples
        if leading_fdb_samples == 0:
            self._state[self._delay_start:self._delay_start + trailing_fdb_samples] = self._state[self._delay_start:self._delay_start + trailing_fdb_samples] * self.feedback + audio[:trailing_fdb_samples]
        else:
            self._state[self._delay_start:self._delay_start + trailing_fdb_samples] = self._state[self._delay_start:self._delay_start + trailing_fdb_samples] * self.feedback + audio[:trailing_fdb_samples]
            self._state[0:leading_fdb_samples] = self._state[0:leading_fdb_samples] * self.feedback + audio[trailing_fdb_samples:]
        self._state = self._state.astype(np.int16) 

        # Track new start of state buffer
        self._delay_start = (self._delay_start + audio.shape[0]) % self._delay_samples

        return output.astype(np.int16)

def main(args):
    global _sample_rate
    print(f"Applying a delay effect to {args.output_audio}")

    _sample_rate = args.sample_rate
    effect = MonoDelay(_sample_rate, args.time, args.feedback, args.mix)

    with wave.open(args.input_audio, 'rb') as inf, wave.open(args.output_audio, 'wb') as outf:
        # Check that sample rate matches expected rate
        if inf.getframerate() != _sample_rate:
            raise Exception(f"Input audio has a sample rate of {inf.getframerate()}, expected {_sample_rate}")

        nchannels, sampwidth, framrate, nframes, _, _ = inf.getparams()
        print(f"Processing {args.input_audio}: ch {nchannels}, width {sampwidth} rate {framrate} samples {nframes}")

        prepare_wav_file(outf)

        for i in range(0, inf.getnframes(), _BLOCK_SIZE):
            block = read_from_wav(inf, _BLOCK_SIZE, mono=(nchannels == 1))
            mono_data = effect.process_mono(block)
            outf.writeframes(mono_data)
