import pyaudio
import numpy as np
from scipy import signal

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
PITCH_SHIFT = 0.8  # Adjust this value to change pitch (>1 for higher, <1 for lower)

p = pyaudio.PyAudio()

# Find the index of your virtual audio device
virtual_device_index = None
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    if "VB-Audio" in dev_info["name"]:  # Change this to match your virtual device name
        virtual_device_index = i
        break

if virtual_device_index is None:
    print("Virtual audio device not found. Please make sure it's installed.")
    exit()

input_stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)

output_stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       output=True,
                       output_device_index=virtual_device_index,
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
        data = np.frombuffer(input_stream.read(CHUNK), dtype=np.float32)
        shifted_data = pitch_shift(data, PITCH_SHIFT, RATE)
        
        # Normalize the output to prevent clipping
        max_val = np.max(np.abs(shifted_data))
        if max_val > 1.0:
            shifted_data /= max_val
        
        output_stream.write(shifted_data.tobytes())
except KeyboardInterrupt:
    print("Stopping...")
finally:
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()