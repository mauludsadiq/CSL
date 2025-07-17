import numpy as np
import soundfile as sf

# Tone parameters
duration = 2.0  # seconds
frequency = 133.87  # Hz (Qasim tone index 17)
sample_rate = 44100  # samples per second

# Time array and waveform
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
tone = 0.5 * np.sin(2 * np.pi * frequency * t)

# Save as WAV file
sf.write('tone_133Hz.wav', tone, sample_rate)
print("✅ Saved: tone_133Hz.wav")
