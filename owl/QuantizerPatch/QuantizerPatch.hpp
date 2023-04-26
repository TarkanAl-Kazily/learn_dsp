/*
 * LICENSE:
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#include "Patch.h"
#include "SignalProcessor.h"
#include "VoltsPerOctave.h"

class Quantizer : public SignalProcessor {
protected:
    static constexpr int kNumChromaticNotes = 12;

public:

    /*
     * Set a user defined scale.
     */
    //void setScale();

    /*
     * Set a linear offset to raise or lower the scale by (after quantizing).
     */
    //void setOffset();

    /*
     * Take an input pitch voltage and output a quantized pitch voltage
     */
    float process(float input) override {
        float temp = input * kNumChromaticNotes;
        int quantized = ((int) (temp + 0.5f));
        return quantized / ((float) kNumChromaticNotes);
    }

    // https://stackoverflow.com/questions/4271245/why-do-i-get-no-matching-function-when-i-inherit-this-function
    using SignalProcessor::process;

    static Quantizer * create() {
        return new Quantizer();
    }

    static void destroy(Quantizer *q) {
        delete q;
    }
};

class QuantizerPatch : public Patch {
public:

    QuantizerPatch() : calibIn(true), calibOut(false) {
        quantizer = Quantizer::create();
    }

    ~QuantizerPatch() {
        Quantizer::destroy(quantizer);
    }

    void processAudio(AudioBuffer &buffer) override;

private:
    Quantizer *quantizer;
    VoltsPerOctave calibIn;
    VoltsPerOctave calibOut;
};
