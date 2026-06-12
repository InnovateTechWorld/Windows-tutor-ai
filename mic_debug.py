"""
mic_debug.py — Records 5 seconds raw from your mic and saves it.
Run this FIRST to verify PyAudio can capture audio at all.
"""
import pyaudio
import wave
import numpy as np

DEVICE_RATE  = 48000
CHANNELS     = 2
CHUNK        = 1024
SECONDS      = 5
OUTPUT_RAW   = "mic_raw_stereo.wav"    # raw 48kHz stereo
OUTPUT_CONV  = "mic_converted_mono.wav" # converted 16kHz mono

pa = pyaudio.PyAudio()

# Print all input devices
print("Input devices:")
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if info["maxInputChannels"] > 0:
        print(f"  [{i}] {info['name']} — max channels: {info['maxInputChannels']}, default rate: {info['defaultSampleRate']}")

mic_idx = int(pa.get_default_input_device_info()["index"])
print(f"\nUsing device [{mic_idx}]. Recording {SECONDS}s — SPEAK NOW...\n")

stream = pa.open(
    format=pyaudio.paInt16,
    channels=CHANNELS,
    rate=DEVICE_RATE,
    input=True,
    input_device_index=mic_idx,
    frames_per_buffer=CHUNK,
)

frames = []
for i in range(0, int(DEVICE_RATE / CHUNK * SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)
    # Print RMS every second to confirm audio is coming in
    if i % int(DEVICE_RATE / CHUNK) == 0:
        samples = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(samples.astype(np.float32)**2))
        print(f"  Second {i // int(DEVICE_RATE/CHUNK) + 1}: RMS={rms:.1f} {'🔇 SILENT!' if rms < 10 else '🎤 OK'}")

stream.stop_stream()
stream.close()

raw_data = b"".join(frames)

# Save raw stereo 48kHz
with wave.open(OUTPUT_RAW, "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(DEVICE_RATE)
    wf.writeframes(raw_data)
print(f"\nSaved raw stereo → {OUTPUT_RAW}")

# Convert stereo 48kHz → mono 16kHz
samples = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32)
stereo  = samples.reshape(-1, 2)
mono    = stereo.mean(axis=1)
# Proper anti-alias + downsample
from numpy.lib.stride_tricks import sliding_window_view
# Simple low-pass: average every 3 samples before decimating
padded = np.pad(mono, (1, 1), mode='edge')
smoothed = (padded[:-2] + padded[1:-1] + padded[2:]) / 3
downsampled = smoothed[::3].astype(np.int16)

with wave.open(OUTPUT_CONV, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(downsampled.tobytes())
print(f"Saved converted mono → {OUTPUT_CONV}")

print("\nDone! Play both WAV files and check if you can hear yourself.")
print("If mic_raw_stereo.wav is also silent → mic permissions or wrong device.")
print("If mic_raw_stereo.wav has audio but mic_converted_mono.wav is silent → conversion bug.")

print("\n--- Testing device 12 (native 16kHz beamformed) ---")
stream12 = pa.open(
    format=pyaudio.paInt16,
    channels=4,
    rate=16000,
    input=True,
    input_device_index=12,
    frames_per_buffer=480,
)
frames12 = []
print("Recording 3s from device 12 — SPEAK NOW...")
for i in range(0, int(16000 / 480 * 3)):
    data = stream12.read(480, exception_on_overflow=False)
    frames12.append(data)
stream12.stop_stream()
stream12.close()

# Convert 4ch → mono
raw12 = b"".join(frames12)
samples12 = np.frombuffer(raw12, dtype=np.int16).astype(np.float32)
mono12 = samples12.reshape(-1, 4).mean(axis=1).astype(np.int16)
with wave.open("mic_device12.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(mono12.tobytes())
print("Saved → mic_device12.wav — play it to verify!")

pa.terminate()
