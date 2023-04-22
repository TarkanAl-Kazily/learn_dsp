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

// Values from AudioBuffer must be scaled by kVoltConst to get volts
constexpr float kVoltConst = - 12.0; // (-0.08) ^ -1

} // anonymous namespace

void MyBasicOscillatorPatch::_handle_parameters(float left_voltage) {
    // Set the frequency from the first parameter
    float freq;

    // https://gahlorddewald.com/hz-to-cv.html
    constexpr float kBaseTuning = 440.0;
    constexpr float kOctaveAdjust = -5.0;
    //constexpr float kFrequencyMultiplier = 2.0;
    constexpr float kAdjustment = 0.0;

    freq = kBaseTuning * fast_exp2f(kOctaveAdjust + getParameterValue(PARAMETER_A) + kAdjustment + left_voltage);
    _oscillator_left->setFrequency(freq);
}

void MyBasicOscillatorPatch::processAudio(AudioBuffer &buffer) {
    FloatArray left = buffer.getSamples(LEFT_CHANNEL);
    FloatArray right = buffer.getSamples(RIGHT_CHANNEL);

    float left_voltage = calib.sampleToVolts(left[0]);
    debugMessage("Sample (V) L", left_voltage);

    // Handle parameters for oscillator
    _handle_parameters(left_voltage);

    // Generate audio

    _oscillator_left->generate(left);
}
