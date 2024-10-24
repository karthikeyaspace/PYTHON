import pyaudio
import numpy as np
from scipy import signal

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
PITCH_SHIFT = 0.8  # Adjust this value to change pitch (>1 for higher, <1 for lower)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("Voice changer running... Press Ctrl+C to stop.")

def pitch_shift(signal, pitch_factor, sample_rate):
    stft = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(len(signal), d=1/sample_rate)
    
    new_freq = freq * pitch_factor
    new_stft = np.zeros_like(stft)
    
    for i in range(len(freq)):
        if new_freq[i] < sample_rate / 2:
            new_index = int(i * pitch_factor)
            if new_index < len(freq):
                new_stft[new_index] = stft[i]
    
    return np.fft.irfft(new_stft).astype(np.float32)

try:
    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.float32)
        shifted_data = pitch_shift(data, PITCH_SHIFT, RATE)
        
        # Normalize the output to prevent clipping
        max_val = np.max(np.abs(shifted_data))
        if max_val > 1.0:
            shifted_data /= max_val
        
        stream.write(shifted_data.tobytes())
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()