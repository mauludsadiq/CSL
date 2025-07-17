import numpy as np
import simpleaudio as sa

def emit_waveform(csl_string):
    sample_rate = 44100
    duration = 0.4  # seconds
    amplitude = 0.3

    # Define CSL frequency map (extend as needed)
    freq_map = {
        "X₁": 110.0,
        "X₂": 111.3,
        "X₃": 112.6,
        "X₄": 114.0,
        "X₅": 116.4,
        "X₆": 118.8,
        "X₇": 121.3,
        "X₈": 143.5,
        "X₉": 145.0,
        "¬X₁": 147.6,
        "¬X₂": 149.3,
        "¬X₃": 151.1,
    }

    tokens = csl_string.replace("·", "").split("]")
    tones = []

    for token in tokens:
        if not token.strip():
            continue
        symbol_power = token.strip().replace("[", "").split("^")
        base = symbol_power[0]
        freq = freq_map.get(base, None)
        if freq:
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            wave = amplitude * np.sin(2 * np.pi * freq * t)
            tones.append(wave)

    if not tones:
        print("⚠️ No valid tones parsed.")
        return

    waveform = np.concatenate(tones)
    waveform = (waveform * 32767).astype(np.int16)
    sa.play_buffer(waveform, 1, 2, sample_rate)
