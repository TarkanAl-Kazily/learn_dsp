/*
 LICENSE:
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
 */


/* created by the OWL team 2013 */

#include "MyBasicOscillatorPatch.hpp"

#include "basicmaths.h"

namespace {

// 


inline float getFreqFromVoltage(float voltage) {
    // https://gahlorddewald.com/hz-to-cv.html
    // Base note to use for tuning (A4)
    constexpr float kBaseTuning = 440.0;
    // How many octaves below base note can be reached
    constexpr float kOctaveAdjust = 5.0;
    // Manual adjustment for the knob so C is approximately in the center
    constexpr float kAdjustment = 0.68;

    return kBaseTuning * fast_exp2f(-kOctaveAdjust + kAdjustment + voltage);
}

} // anonymous namespace

void MyBasicOscillatorPatch::_handle_parameters(float left_voltage) {
    // Set the frequency from the first parameter (detune)
    float freq = getFreqFromVoltage(left_voltage + detune);
    oscillator->setFrequency(freq);

    // Update env parameters
    env->setAttack(attack);
    env->setRelease(decay);
}

void MyBasicOscillatorPatch::processAudio(AudioBuffer &buffer) {
    FloatArray left = buffer.getSamples(LEFT_CHANNEL);

    float left_voltage = calib.sampleToVolts(left[0]);

    // Handle parameters for oscillator
    _handle_parameters(left_voltage);

    // Generate audio
    oscillator->generate(left);

    // Apply envelope as VCA (through convolution)
    env->process(left, left);
}

void MyBasicOscillatorPatch::buttonChanged(PatchButtonId bid, uint16_t value, uint16_t samples) {
    if (bid == BUTTON_A) {
        if (value > 0) {
            // Trigger gate off event in env, starting attack
            env->gate(true);
        } else {
            // Trigger gate off event in env, starting release
            env->gate(false);
        }
    }
}
