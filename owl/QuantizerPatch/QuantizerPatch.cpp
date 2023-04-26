
#include "QuantizerPatch.hpp"

void QuantizerPatch::processAudio(AudioBuffer &buffer) {
    auto samples = buffer.getSamples(LEFT_CHANNEL);
    if (!isButtonPressed(BUTTON_A)) {
        // Convert to voltages
        for (size_t i = 0; i < samples.getSize(); i++) {
            samples[i] = calibIn.sampleToVolts(samples[i]);
        }
        // Quantize voltages
        quantizer->process(samples, samples);
        // Convert back to samples
        for (size_t i = 0; i < samples.getSize(); i++) {
            samples[i] = calibOut.voltsToSample(samples[i]);
        }

        _last_sample = samples[samples.getSize() - 1];
    } else {
        for (size_t i = 0; i < samples.getSize(); i++) {
            samples[i] = _last_sample;
        }
    }
}
