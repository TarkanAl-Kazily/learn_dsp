# Python Experiments

The code in this directory contains experiments for generating and processing audio after the fact.

## Example commands


Amplify the audio file volume by a factor of 10.0
```
python main.py --sample-rate 48000 distortion ../wavs/VoiceNumbers1to10.wav clipped_voice_10.wav --volume 10.0
```

Test stereo WAV math and take a mono sample and make it stereo
```
python main.py --sample-rate 48000 reverb ../wavs/click.wav test.wav --test
```
