/**
 * @file MyBasicOscillatorPatch.hpp
 * @brief Implements a basic square oscillator with built in AR based VCA.
 *
 * Copyright (C) 2023 Tarkan Al-Kazily
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#pragma once

#include "VoltsPerOctave.h"
#include "Patch.h"
#include "SquareWaveOscillator.h"
#include "AdsrEnvelope.h"

/**
 * @brief Implements a basic square oscillator with a built in envelope (Attack Release).
 *
 * Inputs, Outputs:
 * [In, Left] Volt/Octave input to control the pitch of the oscillator.
 *      Expects calibration to be done for the OWL module.
 * [Button / Trigger 1] Gate input for envelope.
 * [Out, Left] Audio out for module.
 *
 * Parameters:
 * [A] Detune, which can be used to tune the oscillator within the octave.
 * [B] Attack time in seconds. Ranges between 0 and 4 seconds.
 * [C] Release time in seconds. Ranges between 0 and 4 seconds.
 */
class MyBasicOscillatorPatch : public Patch {
  public:
    /**
     * Constructor for the patch.
     */
    MyBasicOscillatorPatch() : calib(true) {
        // The order these `getParameter` calls are made in determines which Parameter
        // is assigned to which input (A, B, C).
        detune = getParameter("Detune", 0.5); // A
        attack = getFloatParameter("Attack", 0.0, 4.0, 0.0); // B
        decay = getFloatParameter("Release", 0.0, 4.0, 0.0); // C

        // Allocate all memory in the constructor
        oscillator = SquareWaveOscillator::create(getSampleRate());
        env = LinearAdsrEnvelope::create(getSampleRate());
    }

    /**
     * Destructor.
     */
    ~MyBasicOscillatorPatch() {
        // Delete all memory in the constructor
        SquareWaveOscillator::destroy(oscillator);
        LinearAdsrEnvelope::destroy(env);
    }

    /**
     * @brief Main event loop for OWL patches.
     *
     * All patches must implement processAudio, and this patch is no different.
     * This function handles changes from parameters before processing and generating audio.
     */
    void processAudio(AudioBuffer &buffer) override;

    /**
     * @brief Callback for handling gate / button press events.
     *
     * The two gate inputs are special, and can be handled asynchronously through this callback.
     * This is where the envelope state is updated based on the gate input.
     */
    void buttonChanged(PatchButtonId bid, uint16_t value, uint16_t samples) override;

  private:
    // The oscillator used to generate audio
    SquareWaveOscillator *oscillator;

    // Input parameters used to shape the sound
    FloatParameter detune;
    FloatParameter attack;
    FloatParameter decay;

    // Supports applying offset and multiplication to [-1, 1] signals to a raw voltage level.
    // This is constructed (above) to be associated with the "input", and pulls the stored
    // calibration constants from system memory.
    VoltsPerOctave calib;

    // This is a helper function, called in processAudio, to update all parameters before generating audio
    void _handle_parameters();

    // This ADSR object is used to shape the module's sound in and out.
    // Only the Attack and Release stages are set to non-default values, making it a
    // linear Attack Release envelope.
    LinearAdsrEnvelope *env;
};
