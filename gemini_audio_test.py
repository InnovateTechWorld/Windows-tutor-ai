"""
gemini_audio_test2.py
=====================
Fixed version — uses AUDIO response modality (required by this model).
Saves Gemini's spoken response to response.wav so you can play it back.

USAGE:
  python gemini_audio_test2.py
"""

import asyncio
import os
import wave
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).parent / ".ENV")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .ENV file")

MODEL       = "gemini-2.5-flash-native-audio-preview-12-2025"
INPUT_RATE  = 16000   # Gemini input
OUTPUT_RATE = 24000   # Gemini output


async def test_text_triggers_audio():
    """Test: Send a text message, receive audio response, save to WAV."""
    print("\n" + "="*50)
    print("TEST 1: Text in → Audio out (save to response.wav)")
    print("="*50)

    client = genai.Client(api_key=GEMINI_API_KEY)
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        output_audio_transcription=types.AudioTranscriptionConfig(),
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
            )
        ),
    )

    audio_chunks = []
    transcript   = ""

    try:
        async with client.aio.live.connect(model=MODEL, config=config) as session:
            print("Connected ✅")
            await session.send_realtime_input(
                text="Please say exactly: Hello, this is a test. The audio pipeline is working correctly."
            )
            print("Text sent. Waiting for audio response...")

            async for response in session.receive():
                if response.server_content and response.server_content.model_turn:
                    for part in response.server_content.model_turn.parts:
                        if part.inline_data and part.inline_data.data:
                            audio_chunks.append(part.inline_data.data)
                            print(f"  🔊 Audio chunk: {len(part.inline_data.data)} bytes")

                if response.server_content:
                    sc = response.server_content
                    if sc.output_transcription and sc.output_transcription.text:
                        transcript += sc.output_transcription.text
                        print(f"  📝 Transcript: {sc.output_transcription.text}", end="", flush=True)
                    if sc.generation_complete:
                        print()
                        break

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback; traceback.print_exc()
        return False

    if audio_chunks:
        raw = b"".join(audio_chunks)
        with wave.open("response.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(OUTPUT_RATE)
            wf.writeframes(raw)
        print(f"\n✅ TEST 1 PASSED!")
        print(f"   Audio saved → response.wav ({len(raw)//1024} KB, {len(raw)/OUTPUT_RATE/2:.1f}s)")
        print(f"   Transcript: '{transcript}'")
        print(f"   ▶️  Play response.wav to hear Gemini's voice")
        return True
    else:
        print("\n❌ TEST 1 FAILED — No audio received")
        return False


async def test_audio_in_audio_out():
    """Test: Send mic_test.wav audio → receive audio response."""
    print("\n" + "="*50)
    print("TEST 2: Audio in → Audio out")
    print("="*50)

    # Load mic_converted_mono.wav
    mic_wav = Path("mic_converted_mono.wav")
    if not mic_wav.exists():
        print("⚠️  mic_converted_mono.wav not found — skipping audio input test")
        return

    with wave.open(str(mic_wav), "rb") as wf:
        channels = wf.getnchannels()
        rate     = wf.getframerate()
        raw      = wf.readframes(wf.getnframes())

    print(f"Loaded mic_converted_mono.wav: {channels}ch {rate}Hz {len(raw)//1024}KB ({len(raw)/rate/2:.1f}s)")

    # Convert to mono 16kHz
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    if channels == 2:
        samples = samples.reshape(-1, 2).mean(axis=1)
    if rate != INPUT_RATE:
        new_len = int(len(samples) * INPUT_RATE / rate)
        samples = np.interp(
            np.linspace(0, len(samples)-1, new_len),
            np.arange(len(samples)), samples
        )
    audio_in = samples.astype(np.int16).tobytes()
    print(f"Converted to mono 16kHz: {len(audio_in)//1024}KB")

    client = genai.Client(api_key=GEMINI_API_KEY)
    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
        realtime_input_config=types.RealtimeInputConfig(
            automatic_activity_detection=types.AutomaticActivityDetection(
                disabled=False,
                start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_LOW,
                end_of_speech_sensitivity=types.EndSensitivity.END_SENSITIVITY_HIGH,
                prefix_padding_ms=200,
                silence_duration_ms=800,
            )
        ),
        system_instruction="You are a helpful assistant. Listen carefully and respond to what the user says.",
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
            )
        ),
    )

    audio_out_chunks = []
    in_transcript    = ""
    out_transcript   = ""

    try:
        async with client.aio.live.connect(model=MODEL, config=config) as session:
            print("Connected ✅")
            print("Sending audio file in 30ms chunks...")

            # Send audio in real-time chunks
            CHUNK = INPUT_RATE * 2 * 30 // 1000  # 30ms of bytes
            sent  = 0
            for i in range(0, len(audio_in), CHUNK):
                chunk = audio_in[i:i+CHUNK]
                if not chunk:
                    break
                await session.send_realtime_input(
                    audio=types.Blob(data=chunk, mime_type=f"audio/pcm;rate={INPUT_RATE}")
                )
                sent += 1
                await asyncio.sleep(0.03)

            print(f"Sent {sent} chunks. Waiting 2s for VAD to finalize...")
            await asyncio.sleep(2.0)

            # Text nudge to ensure response
            print("Sending text nudge...")
            await session.send_realtime_input(
                text="Please respond to what you just heard."
            )

            print("Collecting response (15s timeout)...")
            try:
                async with asyncio.timeout(15):
                    async for response in session.receive():
                        if response.server_content and response.server_content.model_turn:
                            for part in response.server_content.model_turn.parts:
                                if part.inline_data and part.inline_data.data:
                                    audio_out_chunks.append(part.inline_data.data)
                                    print(f"  🔊 {len(part.inline_data.data)} bytes", end=" ", flush=True)

                        if response.server_content:
                            sc = response.server_content
                            if sc.input_transcription and sc.input_transcription.text:
                                in_transcript += sc.input_transcription.text
                                print(f"\n  🗣️  You said: '{sc.input_transcription.text}'")
                            if sc.output_transcription and sc.output_transcription.text:
                                out_transcript += sc.output_transcription.text
                                print(f"  🤖 Gemini: '{sc.output_transcription.text}'", end="", flush=True)
                            if sc.generation_complete:
                                print()
                                break
            except asyncio.TimeoutError:
                print("\n(timeout)")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback; traceback.print_exc()
        return

    print("\n--- RESULTS ---")
    if in_transcript:
        print(f"✅ Gemini heard you say: '{in_transcript}'")
    else:
        print("❌ No speech detected in mic_test.wav")
        print("   → The WAV file either has no speech or speech is too quiet")
        print("   → Re-run the app with SAVE_MIC_WAV=True and speak loudly")

    if audio_out_chunks:
        raw_out = b"".join(audio_out_chunks)
        with wave.open("response2.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(OUTPUT_RATE)
            wf.writeframes(raw_out)
        print(f"✅ Gemini responded! Saved → response2.wav")
        print(f"   Gemini said: '{out_transcript}'")
    else:
        print("❌ No audio response from Gemini")


async def main():
    print("Gemini Live Audio Test v2")
    print(f"Model: {MODEL}")
    print(f"API key: {GEMINI_API_KEY[:8]}...{GEMINI_API_KEY[-4:]}")

    ok = await test_text_triggers_audio()
    if ok:
        print("\n▶️  Play response.wav NOW to confirm you can hear Gemini's voice")
        input("   Press Enter when done listening...")
        await test_audio_in_audio_out()

    print("\n" + "="*50)
    print("DONE")
    print("="*50)


if __name__ == "__main__":
    asyncio.run(main())