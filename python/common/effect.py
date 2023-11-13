# Copyright 2023 Tarkan Al-Kazily 

class Effect:
    """
    Base (abstract) class for applying effects to audio

    Attributes:
    - sample_rate: Sample rate for all audio
    """

    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

    def process_mono(self, audio):
        """
        Applies an effect to (mono) audio

        Arguments:
        - audio: Numpy array of samples to process
        
        Returns:
        - Numpy array of the processed audio
        """
        pass
