
#include "QuantizerPatch.hpp"

void QuantizerPatch::processAudio(AudioBuffer &buffer) {
    // Convert to voltages
    auto samples = buffer.getSamples(LEFT_CHANNEL);
    for (size_t i = 0; i < samples.getSize(); i++) {
        samples[i] = calibIn.sampleToVolts(samples[i]);
    }
    // Quantize voltages
    quantizer->process(samples, samples);
    // Convert back to samples
    for (size_t i = 0; i < samples.getSize(); i++) {
        samples[i] = calibOut.voltsToSample(samples[i]);
    }
}
