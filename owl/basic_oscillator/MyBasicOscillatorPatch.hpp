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

#pragma once

#include "VoltsPerOctave.h"
#include "Patch.h"
#include "SquareWaveOscillator.h"
#include "AdsrEnvelope.h"

class MyBasicOscillatorPatch : public Patch {
public:
  MyBasicOscillatorPatch() {
    detune = getParameter("Detune", 0.5); // A
    attack = getFloatParameter("Attack", 0.0, 4.0, 0.0); // B
    decay = getFloatParameter("Release", 0.0, 4.0, 0.0); // C

    // Create / allocate all memory in the constructor
    oscillator = SquareWaveOscillator::create(getSampleRate());
    env = LinearAdsrEnvelope::create(getSampleRate());
  }

  ~MyBasicOscillatorPatch() {
    // Delete all memory in the constructor
    SquareWaveOscillator::destroy(oscillator);
    LinearAdsrEnvelope::destroy(env);
  }
 
  void processAudio(AudioBuffer &buffer) override;

  void buttonChanged(PatchButtonId bid, uint16_t value, uint16_t samples) override;

private:
  SquareWaveOscillator *oscillator;

  FloatParameter detune;
  FloatParameter attack;
  FloatParameter decay;

  VoltsPerOctave calib;

  // Called in processAudio to update all the parameters before generating audio
  void _handle_parameters(float left_voltage);

  LinearAdsrEnvelope *env;
};
