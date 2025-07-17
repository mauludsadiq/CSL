import numpy as np
import simpleaudio as sa

def emit_waveform(phrase):
    tone_map = {
        'A': 110.0, 'B': 111.278, 'C': 112.571,
        'X': 143.479, 'Y': 145.146, 'Z': 146.832,
        '1': 120.0, '2': 122.5, '3': 125.0,
        '4': 127.5, '5': 130.0, '6': 132.5,
        '7': 135.0, '8': 137.5, '9': 140.0,
        '¬': 100.0
    }

    sample_rate = 44100
    duration = 0.18  # shortened for safety
    amplitude = 0.4

    # Sanitize: remove brackets and delimiters
    clean = ''.join(filter(lambda c: c.isalnum() or c == '¬', phrase))

    wave = np.array([], dtype=np.float32)

    for char in clean:
        freq = tone_map.get(char.upper())
        if not freq:
            continue
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = amplitude * np.sin(2 * np.pi * freq * t)
        wave = np.concatenate((wave, tone))

    wave = (wave * 32767 / np.max(np.abs(wave))).astype(np.int16)
    sa.play_buffer(wave, 1, 2, sample_rate)
