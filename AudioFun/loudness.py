import pyaudio
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Listening for loudness... Press Ctrl+C to stop.")

def calculate_rms(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    if len(audio_data) == 0:
        return 0
    # Convert to float to avoid overflow
    audio_data_float = audio_data.astype(np.float64) 
    rms = np.sqrt(np.mean(audio_data_float**2))
    return rms

try:
    while True:
        data = stream.read(CHUNK)
        if len(data) != CHUNK * 2:
            continue
        rms_loudness = calculate_rms(data)
        rms_loudness = int(rms_loudness)
        lines = rms_loudness // 1000
        if lines==0:
            print("|")
        else:
            print("|" * lines)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()