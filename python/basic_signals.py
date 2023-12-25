# Copyright 2023 Tarkan Al-Kazily

import wave
import enum
import numpy as np

# global sample rate in Hz
_sample_rate = 44100

def prepare_wav_file(f):
    f.setframerate(_sample_rate)
    f.setnchannels(1)
    f.setsampwidth(2)

class BasicSignal(enum.Enum):
    """
    Enum describing the basic signal types

    * DC_STEP is a 0 -> 1 step between two constant signals
    * NYQUIST is the signal { ... -1 +1 -1 +1 -1 ... } that represents the nyquist frequency
    * HALF_NYQUIST is the signal representing half the nyquist frequency { ... -1 0 1 0 -1 ...}
    * QUARTER_NYQUIST is the signal representing one quarter the nyquist frequency { ... -1 -0.707 0 .707 1 0.707 0 -0.707 -1 ...}
    * IMPULSE is a single sample 1 in an infinitely long stream of 0 { ... 0 0 0 0 1 0 0 0 ... }
    """
    DC_STEP = 1
    NYQUIST = 2
    HALF_NYQUIST = 3
    QUARTER_NYQUIST = 4
    IMPULSE = 5

def _generate_dc_step(array):
    """
    Modifies array to generate a DC_STEP signal

    Args:
       array: 1d array of floats to use to store result in. The shape defines the size of the generated signal
    """
    for i in range(array.shape[0]):
        if i < array.shape[0] / 2:
            array[i] = 0.0
        else:
            array[i] = 1.0

def _generate_nyquist(array):
    """
    Modifies array to generate a NYQUIST signal

    Args:
       array: 1d array of floats to use to store result in. The shape defines the size of the generated signal
    """
    for i in range(array.shape[0]):
        if i % 2 == 0:
            array[i] = -1.0
        else:
            array[i] = 1.0

def _generate_half_nyquist(array):
    """
    Modifies array to generate a HALF_NYQUIST signal

    Args:
       array: 1d array of floats to use to store result in. The shape defines the size of the generated signal
    """
    for i in range(array.shape[0]):
        if i % 4 == 0:
            array[i] = -1.0
        elif i % 4 in {1, 3}:
            array[i] = 0.0
        else:
            array[i] = 1.0

def _generate_quarter_nyquist(array):
    """
    Modifies array to generate a QUARTER_NYQUIST Signal

    Args:
       array: 1d array of floats to use to store result in. The shape defines the size of the generated signal
    """
    COS_PI_4 = 0.707
    for i in range(array.shape[0]):
        if i % 8 == 0:
            array[i] = -1.0
        elif i % 8 in {1, 7}:
            array[i] = -COS_PI_4
        elif i % 8 in {2, 6}:
            array[i] = 0.0
        elif i % 8 in {3, 5}:
            array[i] = COS_PI_4
        else:
            array[i] = 1.0

def _generate_impulse(array):
    """
    Modifies array to generate a IMPULSE signal

    Args:
       array: 1d array of floats to use to store result in. The shape defines the size of the generated signal
    """
    midpoint = int(array.shape[0] / 2)
    array[midpoint] = 1.0

def generate_signal(signal_type : BasicSignal , duration_s=1.0):
    """
    Generates a basic signal - see BasicSignal for a description of the signal types

    Args:
        duration_s (optional): duration of the output signal in seconds.
        signal_type: BasicSignal type of signal to generate.

    Returns:
        np array with the generated signal
    """
    samples = int(_sample_rate * duration_s + 1)
    result = np.zeros(samples, dtype=np.float16)

    _funcs = {
        BasicSignal.DC_STEP : _generate_dc_step,
        BasicSignal.NYQUIST : _generate_nyquist,
        BasicSignal.HALF_NYQUIST : _generate_half_nyquist,
        BasicSignal.QUARTER_NYQUIST : _generate_quarter_nyquist,
        BasicSignal.IMPULSE : _generate_impulse,
    }

    _funcs[signal_type](result)
    return result

def convert_float_arr_to_int(array : np.array):
    """
    Converts an array from a float signal between [-1.0, 1.0] to an integer array between [-32768, 32767] (16 bits)
    Args:
        array: float type array to convert to int16 type array

    Returns:
        New np.array
    """
    BIT_WIDTH = 16
    result = np.asarray(array * (2 ** (BIT_WIDTH - 1) - 1), dtype=np.int16)

    return result

def main(args):
    print(f"Generating basic oscillator waves to {args.filename}")

    _sample_rate = args.sample_rate

    with wave.open(args.filename, 'wb') as f:
        prepare_wav_file(f)
        data = generate_signal(signal_type=BasicSignal(args.signal_type), duration_s=100 / _sample_rate)
        int_data = convert_float_arr_to_int(data)
        f.writeframes(int_data)

