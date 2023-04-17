import wave
import enum
import numpy as np

# global sample rate in Hz
_sample_rate = 44100

class BasicWave(enum.Enum):
    SINE = 1
    SQUARE = 2
    SAW = 3
    TRIANGLE = 4

def prepare_wav_file(f):
    f.setframerate(_sample_rate)
    f.setnchannels(1)
    f.setsampwidth(2)

def generate_wave(type=BasicWave.SINE, frequency=440.0, duration_s=1.0):
    """
    f: File to write wave to
    type: Type of wave to generate
    frequency: Tone of wave to generate
    duration_s: Time in seconds for wave

    returns numpy array of data
    """

    samples = int(_sample_rate * duration_s + 1)
    result = np.empty(samples)

    samples_per_period = int(_sample_rate / frequency)
    for i in range(samples):
        result[i] = i % samples_per_period
    result = result / (2.0 * np.pi * samples_per_period)
    result = np.sin(result) * 4096.0 # 2**12

    return np.asarray(result, dtype=np.int16)


def main(args):
    print(f"Generating basic oscillator waves to {args.filename}")

    _sample_rate = args.sample_rate

    with wave.open(args.filename, 'wb') as f:
        prepare_wav_file(f)
        data = generate_wave(type=BasicWave.SINE, frequency=args.frequency)
        f.writeframes(data)
