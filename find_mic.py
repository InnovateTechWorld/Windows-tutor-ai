"""
find_mic_wasapi.py — Scans WASAPI devices (the correct backend for modern Windows).
The -9999 errors you saw were because PyAudio was using MME backend.
WASAPI gives direct access to the actual Realtek hardware.
"""
import pyaudio
import wave
import numpy as np

pa = pyaudio.PyAudio()

# Get WASAPI host API index
wasapi_index = None
for i in range(pa.get_host_api_count()):
    info = pa.get_host_api_info_by_index(i)
    print(f"Host API [{i}]: {info['name']}  devices={info['deviceCount']}")
    if "WASAPI" in info["name"]:
        wasapi_index = i

print()

if wasapi_index is None:
    print("❌ WASAPI not found! Check your PyAudio installation.")
    pa.terminate()
    exit()

print(f"✅ WASAPI found at host API index {wasapi_index}")
print("=" * 60)
print("Scanning WASAPI input devices...")
print("=" * 60)

wasapi_info = pa.get_host_api_info_by_index(wasapi_index)
working = []

CHUNK = 480
RECORD_SECONDS = 3

for i in range(pa.get_device_count()):
    dev = pa.get_device_info_by_index(i)

    # Only WASAPI devices
    if dev["hostApi"] != wasapi_index:
        continue
    if dev["maxInputChannels"] < 1:
        continue

    name = dev["name"]
    default_rate = int(dev["defaultSampleRate"])
    max_ch = dev["maxInputChannels"]

    print(f"\n[{i}] {name}")
    print(f"     max_ch={max_ch}  default_rate={default_rate}")

    # Try configs — prioritize 16kHz mono, fall back to native rate
    configs = [
        {"rate": 16000,       "channels": 1},
        {"rate": 16000,       "channels": min(2, max_ch)},
        {"rate": default_rate,"channels": 1},
        {"rate": default_rate,"channels": min(2, max_ch)},
        {"rate": 48000,       "channels": 1},
        {"rate": 44100,       "channels": 1},
    ]
    # Deduplicate
    seen = set()
    unique_configs = []
    for c in configs:
        key = (c["rate"], c["channels"])
        if key not in seen:
            seen.add(key)
            unique_configs.append(c)

    for cfg in unique_configs:
        rate = cfg["rate"]
        chans = cfg["channels"]
        try:
            stream = pa.open(
                format=pyaudio.paInt16,
                channels=chans,
                rate=rate,
                input=True,
                input_device_index=i,
                frames_per_buffer=CHUNK,
                input_host_api_specific_stream_info=None,
            )
            frames = []
            total_chunks = int(rate / CHUNK * RECORD_SECONDS)
            for _ in range(total_chunks):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            stream.stop_stream()
            stream.close()

            raw = b"".join(frames)
            samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
            rms = np.sqrt(np.mean(samples**2))
            print(f"     ✅ {rate}Hz {chans}ch — RMS={rms:.1f} {'🎤 has audio!' if rms > 50 else '🔇 silent'}")

            working.append({
                "index": i,
                "name": name,
                "rate": rate,
                "channels": chans,
                "rms": rms,
                "default_rate": default_rate,
            })
            break  # only log first working config per device

        except Exception as e:
            print(f"     ❌ {rate}Hz {chans}ch — {str(e)[:70]}")

pa.terminate()

print("\n" + "=" * 60)
print("WORKING WASAPI DEVICES:")
print("=" * 60)
for d in working:
    audio = "🎤 has audio" if d["rms"] > 50 else "🔇 silent/idle"
    print(f"  [{d['index']}] {d['name']}")
    print(f"       {d['rate']}Hz {d['channels']}ch  RMS={d['rms']:.1f}  {audio}")

if working:
    # Best = highest RMS among those that work at 16kHz, else highest RMS overall
    at_16k = [d for d in working if d["rate"] == 16000]
    pool = at_16k if at_16k else working
    best = max(pool, key=lambda x: x["rms"])
    print(f"\n⭐ BEST DEVICE: [{best['index']}] {best['name']}")
    print(f"   MIC_DEVICE_INDEX = {best['index']}")
    print(f"   MIC_DEVICE_RATE  = {best['rate']}")
    print(f"   MIC_DEVICE_CHANS = {best['channels']}")
    print(f"\n   Paste these 3 lines into tutor_live.py config section.")
else:
    print("\n❌ No working WASAPI input devices found.")
    print("   Try: Settings → Privacy & Security → Microphone → Allow apps to access microphone ✅")