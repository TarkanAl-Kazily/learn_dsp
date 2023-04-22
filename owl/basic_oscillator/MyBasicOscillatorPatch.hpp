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

#include "Patch.h"
#include "SquareWaveOscillator.h"

class MyBasicOscillatorPatch : public Patch {
public:
  MyBasicOscillatorPatch() {
    registerParameter(PARAMETER_A, "Detune Offset");
    registerParameter(PARAMETER_B, "My Knob B");
    registerParameter(PARAMETER_C, "My Knob C");
    registerParameter(PARAMETER_D, "My Knob D");

    // Create / allocate all memory in the constructor
    _oscillator = SquareWaveOscillator::create(getSampleRate());
  }

  ~MyBasicOscillatorPatch() {
    // Delete all memory in the constructor
    SquareWaveOscillator::destroy(_oscillator);
  }
 
  void processAudio(AudioBuffer &buffer) override;

private:
  SquareWaveOscillator *_oscillator;

  // Called in processAudio to update all the parameters before generating audio
  void _handle_parameters();
};
