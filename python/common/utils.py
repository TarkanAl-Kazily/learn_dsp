# Copyright 2023 Tarkan Al-Kazily 

import numpy as np

_BLOCK_SIZE = 2 ** 12

def read_from_wav(f, n, mono=False, channel=0):
    """
    Returns a bytearray from a wav file on the given channel (the other channel is discarded)

    # Standard for the wav file format
    # https://web.archive.org/web/20140221054954/http://home.roadrunner.com/~jgglatt/tech/wave.htm
    # Drop right half of audio
    """
    b = f.readframes(n)
    block = np.frombuffer(b, dtype=np.int16)
    if mono:
        return block

    block = np.reshape(block, (int(block.shape[0] / 2), 2))
    return block[:,channel]

def stereo_to_frames(block):
    """
    Returns a bytearray suitable to writeframes to a file for a stereo block of audio
    """
    if block.shape[1] != 2:
        raise Exception(f"Expected block to be stereo, but has shape {block.shape}")

    # reshape into a single buffer 16 bit
    result = np.reshape(block, block.shape[0] * 2)
    return result
