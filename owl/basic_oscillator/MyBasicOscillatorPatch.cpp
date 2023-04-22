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

void MyBasicOscillatorPatch::_handle_parameters() {
    // Set the frequency from the first parameter
    float freq;


    // https://gahlorddewald.com/hz-to-cv.html
    constexpr float kBaseTuning = 440.0;
    constexpr float kLowestOctave = 8.0;
    //constexpr float kFrequencyMultiplier = 2.0;
    constexpr float kAdjustment = 0.66;

    freq = (kBaseTuning / kLowestOctave) * fast_exp2f(getParameterValue(PARAMETER_A) + kAdjustment);

    _oscillator->setFrequency(freq);
}

void MyBasicOscillatorPatch::processAudio(AudioBuffer &buffer) {
    // Handle parameters for oscillator
    _handle_parameters();

    // Generate audio
    FloatArray left = buffer.getSamples(LEFT_CHANNEL);
    FloatArray right = buffer.getSamples(RIGHT_CHANNEL);

    _oscillator->generate(left);
}
