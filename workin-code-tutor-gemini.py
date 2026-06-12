"""
Windows Tutor AI — Gemini Live Edition
=======================================
Based on Google's official working example + screen sharing + Tkinter UI.

CONTROLS:
  - Talk naturally — VAD detects speech automatically
  - Ctrl+Space — manually trigger screen description
  - Ctrl+C or close window — quit

REQUIREMENTS:
  pip install google-genai pyaudio mss pywinauto pillow keyboard python-dotenv
"""

import asyncio
import ctypes
import io
import math
import os
import queue
import signal
import threading
import time
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path

import keyboard
import mss
import pyaudio
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image, ImageTk
from pywinauto import Application

# ─────────────────────────────────────────────────────────────────────────────
# LOAD ENV
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv(Path(__file__).parent / ".ENV")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .ENV file")

client = genai.Client(api_key=GEMINI_API_KEY)

# ─────────────────────────────────────────────────────────────────────────────
# AUDIO CONFIG  (exactly as Google's working example)
# ─────────────────────────────────────────────────────────────────────────────
FORMAT            = pyaudio.paInt16
CHANNELS          = 1
SEND_SAMPLE_RATE  = 16000
RECV_SAMPLE_RATE  = 24000
CHUNK_SIZE        = 1024

pya = pyaudio.PyAudio()

# ─────────────────────────────────────────────────────────────────────────────
# GEMINI CONFIG
# ─────────────────────────────────────────────────────────────────────────────
MODEL = "gemini-3.1-flash-live-preview"

SYSTEM_INSTRUCTION = """You are an AI tutor and assistant running on a Windows PC.
You can SEE the user's screen (screenshots every second) and HEAR them speak.
The user can hear your voice through their speakers.

Your personality:
- Warm, encouraging, and conversational
- Concise — 1 to 3 sentences unless more detail is needed
- Proactive — if you see something interesting on screen, mention it
- Helpful — guide the user step by step when they need help

When you see the screen:
- Describe what you observe when relevant
- Point out things the user might find useful
- Help them navigate software or understand what's on screen

When the user speaks:
- Respond naturally to everything they say
- If they ask about something on screen, describe it clearly
- Use simple language and avoid jargon unless the user is technical

Start by greeting the user warmly and briefly describing what you see on their screen."""

CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction=SYSTEM_INSTRUCTION,
    output_audio_transcription=types.AudioTranscriptionConfig(),
    input_audio_transcription=types.AudioTranscriptionConfig(),
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
        )
    ),
    realtime_input_config=types.RealtimeInputConfig(
        automatic_activity_detection=types.AutomaticActivityDetection(
            disabled=False,
            start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_HIGH,
            end_of_speech_sensitivity=types.EndSensitivity.END_SENSITIVITY_LOW,
            prefix_padding_ms=20,
            silence_duration_ms=600,
        )
    ),
    context_window_compression=types.ContextWindowCompressionConfig(
        sliding_window=types.SlidingWindow(),
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# DPI AWARENESS
# ─────────────────────────────────────────────────────────────────────────────
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN CAPTURE
# ─────────────────────────────────────────────────────────────────────────────
def capture_screen_jpeg(quality=35):
    with mss.mss() as sct:
        raw = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", raw.size, raw.rgb)
        img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality)
        return buf.getvalue()

# ─────────────────────────────────────────────────────────────────────────────
# TKINTER UI
# ─────────────────────────────────────────────────────────────────────────────
class TutorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows Tutor AI")
        self.root.geometry("420x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f0f")

        # Keep on top option
        self.always_on_top = tk.BooleanVar(value=True)
        self.root.attributes("-topmost", True)

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._shutdown_callback = None
        self.status_var = tk.StringVar(value="Connecting…")

    def set_shutdown_callback(self, cb):
        self._shutdown_callback = cb

    def _on_close(self):
        if self._shutdown_callback:
            self._shutdown_callback()
        self.root.destroy()

    def _build_ui(self):
        # ── Header ────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg="#0f0f0f", pady=16)
        header.pack(fill="x", padx=20)

        # Logo dot + title
        title_row = tk.Frame(header, bg="#0f0f0f")
        title_row.pack(fill="x")

        self.status_dot = tk.Canvas(title_row, width=12, height=12,
                                     bg="#0f0f0f", highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 8))
        self._dot_oval = self.status_dot.create_oval(2, 2, 10, 10, fill="#333", outline="")

        tk.Label(title_row, text="Windows Tutor AI",
                 font=("Segoe UI", 15, "bold"),
                 fg="#ffffff", bg="#0f0f0f").pack(side="left")

        # Status label
        self.status_label = tk.Label(header, textvariable=tk.StringVar(value=""),
                                      font=("Segoe UI", 9),
                                      fg="#666", bg="#0f0f0f")
        self.status_label.pack(anchor="w", pady=(4, 0))
        self._status_str = tk.StringVar(value="Connecting…")
        self.status_label.configure(textvariable=self._status_str)

        # Divider
        tk.Frame(self.root, bg="#1e1e1e", height=1).pack(fill="x", padx=20)

        # ── Transcript area ───────────────────────────────────────────────
        transcript_frame = tk.Frame(self.root, bg="#0f0f0f")
        transcript_frame.pack(fill="both", expand=True, padx=12, pady=10)

        self.transcript = tk.Text(
            transcript_frame,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#111111",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            relief="flat",
            padx=12,
            pady=10,
            state="disabled",
            cursor="arrow",
        )
        self.transcript.pack(fill="both", expand=True)

        # Tags for styling
        self.transcript.tag_configure("you",    foreground="#60a5fa", font=("Segoe UI", 10, "bold"))
        self.transcript.tag_configure("gemini", foreground="#34d399", font=("Segoe UI", 10, "bold"))
        self.transcript.tag_configure("you_text",    foreground="#bfdbfe")
        self.transcript.tag_configure("gemini_text", foreground="#a7f3d0")
        self.transcript.tag_configure("system", foreground="#555", font=("Segoe UI", 9, "italic"))

        # Scrollbar
        scrollbar = tk.Scrollbar(transcript_frame, command=self.transcript.yview,
                                  bg="#1e1e1e", troughcolor="#111", width=6)
        self.transcript.configure(yscrollcommand=scrollbar.set)

        # ── Divider ────────────────────────────────────────────────────────
        tk.Frame(self.root, bg="#1e1e1e", height=1).pack(fill="x", padx=20)

        # ── Controls ──────────────────────────────────────────────────────
        controls = tk.Frame(self.root, bg="#0f0f0f", pady=14)
        controls.pack(fill="x", padx=20)

        # Screen preview toggle
        self.show_preview = tk.BooleanVar(value=False)
        preview_btn = tk.Checkbutton(
            controls, text="Screen preview",
            variable=self.show_preview,
            command=self._toggle_preview,
            bg="#0f0f0f", fg="#888", activebackground="#0f0f0f",
            activeforeground="#fff", selectcolor="#1a1a1a",
            font=("Segoe UI", 9),
        )
        preview_btn.pack(side="left")

        # Always on top toggle
        aot_btn = tk.Checkbutton(
            controls, text="Always on top",
            variable=self.always_on_top,
            command=self._toggle_aot,
            bg="#0f0f0f", fg="#888", activebackground="#0f0f0f",
            activeforeground="#fff", selectcolor="#1a1a1a",
            font=("Segoe UI", 9),
        )
        aot_btn.pack(side="left", padx=(16, 0))

        # Ctrl+Space button
        snap_btn = tk.Button(
            controls, text="⌨ Describe Screen",
            command=self._on_snap_click,
            bg="#1a1a1a", fg="#888",
            activebackground="#222", activeforeground="#fff",
            relief="flat", font=("Segoe UI", 9),
            padx=10, pady=4,
        )
        snap_btn.pack(side="right")

        # ── Screen preview panel (hidden by default) ─────────────────────
        self.preview_frame = tk.Frame(self.root, bg="#0f0f0f")
        self.preview_label = tk.Label(self.preview_frame, bg="#111", relief="flat")
        self.preview_label.pack(padx=8, pady=8)

        # ── Footer ────────────────────────────────────────────────────────
        footer = tk.Frame(self.root, bg="#0a0a0a", pady=8)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer, text="Ctrl+Space  =  describe screen  •  Ctrl+C  =  quit",
                 font=("Segoe UI", 8), fg="#333", bg="#0a0a0a").pack()

    def _toggle_aot(self):
        self.root.attributes("-topmost", self.always_on_top.get())

    def _toggle_preview(self):
        if self.show_preview.get():
            self.preview_frame.pack(fill="x", padx=12, before=self.root.winfo_children()[-1])
        else:
            self.preview_frame.pack_forget()

    def _on_snap_click(self):
        if self._snap_callback:
            self._snap_callback()

    _snap_callback = None

    def set_snap_callback(self, cb):
        self._snap_callback = cb

    # ── Public methods ────────────────────────────────────────────────────
    def set_status(self, text, color="#666"):
        self.root.after(0, lambda: self._status_str.set(text))

    def set_dot(self, color):
        self.root.after(0, lambda: self.status_dot.itemconfig(self._dot_oval, fill=color))

    def add_message(self, speaker, text):
        """Add a transcript message. speaker = 'you' | 'gemini' | 'system'"""
        def _do():
            self.transcript.configure(state="normal")
            if speaker == "you":
                self.transcript.insert("end", "You\n", "you")
                self.transcript.insert("end", text + "\n\n", "you_text")
            elif speaker == "gemini":
                self.transcript.insert("end", "Gemini\n", "gemini")
                self.transcript.insert("end", text + "\n\n", "gemini_text")
            else:
                self.transcript.insert("end", text + "\n", "system")
            self.transcript.configure(state="disabled")
            self.transcript.see("end")
        self.root.after(0, _do)

    def update_preview(self, jpeg_bytes):
        """Update the screen preview thumbnail."""
        if not self.show_preview.get():
            return
        def _do():
            try:
                img = Image.open(io.BytesIO(jpeg_bytes))
                img.thumbnail((380, 220), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.preview_label.configure(image=photo)
                self.preview_label._photo = photo  # keep reference
            except Exception:
                pass
        self.root.after(0, _do)

    def animate_listening(self):
        """Pulse the status dot green while listening."""
        self._pulse(0)

    def _pulse(self, n):
        if n % 2 == 0:
            self.set_dot("#22c55e")
        else:
            self.set_dot("#166534")
        self.root.after(600, lambda: self._pulse(n + 1))

    def mainloop(self):
        self.root.mainloop()

    def quit(self):
        try:
            self.root.quit()
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# GLOBALS
# ─────────────────────────────────────────────────────────────────────────────
audio_queue_output = asyncio.Queue()
audio_queue_mic    = asyncio.Queue(maxsize=5)
hotkey_queue: asyncio.Queue | None = None
audio_stream_in    = None
_shutdown          = threading.Event()
ui: TutorUI | None = None


# ─────────────────────────────────────────────────────────────────────────────
# AUDIO TASKS  (identical to Google's working example)
# ─────────────────────────────────────────────────────────────────────────────
async def listen_audio():
    global audio_stream_in
    mic_info = pya.get_default_input_device_info()
    audio_stream_in = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=SEND_SAMPLE_RATE,
        input=True,
        input_device_index=mic_info["index"],
        frames_per_buffer=CHUNK_SIZE,
    )
    while not _shutdown.is_set():
        data = await asyncio.to_thread(
            audio_stream_in.read, CHUNK_SIZE, exception_on_overflow=False
        )
        await audio_queue_mic.put({"data": data, "mime_type": "audio/pcm"})


async def send_audio(session):
    while not _shutdown.is_set():
        msg = await audio_queue_mic.get()
        await session.send_realtime_input(audio=msg)


async def play_audio():
    stream = await asyncio.to_thread(
        pya.open,
        format=FORMAT,
        channels=CHANNELS,
        rate=RECV_SAMPLE_RATE,
        output=True,
    )
    while not _shutdown.is_set():
        data = await audio_queue_output.get()
        await asyncio.to_thread(stream.write, data)


# ─────────────────────────────────────────────────────────────────────────────
# SCREEN TASK
# ─────────────────────────────────────────────────────────────────────────────
async def send_screen(session):
    loop = asyncio.get_running_loop()
    n = 0
    while not _shutdown.is_set():
        try:
            jpeg = await loop.run_in_executor(None, capture_screen_jpeg)
            await session.send_realtime_input(
                video=types.Blob(data=jpeg, mime_type="image/jpeg")
            )
            n += 1
            if ui:
                ui.update_preview(jpeg)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"[screen] {e}")
        await asyncio.sleep(1.0)


# ─────────────────────────────────────────────────────────────────────────────
# HOTKEY TASK
# ─────────────────────────────────────────────────────────────────────────────
async def hotkey_loop(session):
    loop = asyncio.get_running_loop()
    while not _shutdown.is_set():
        try:
            await asyncio.wait_for(hotkey_queue.get(), timeout=0.5)
        except asyncio.TimeoutError:
            continue
        except asyncio.CancelledError:
            break
        try:
            jpeg = await loop.run_in_executor(None, capture_screen_jpeg)
            await session.send_realtime_input(
                video=types.Blob(data=jpeg, mime_type="image/jpeg")
            )
            await session.send_realtime_input(
                text="Please look at my screen right now and describe what you see and what I should do next."
            )
            if ui:
                ui.set_status("Screen snapshot sent…", "#f59e0b")
        except Exception as e:
            print(f"[hotkey] {e}")


# ─────────────────────────────────────────────────────────────────────────────
# RECEIVE TASK
# ─────────────────────────────────────────────────────────────────────────────
async def receive_responses(session):
    you_buf    = ""
    gemini_buf = ""
    last_was_input = False

    while not _shutdown.is_set():
        turn = session.receive()
        async for response in turn:
            sc = response.server_content
            if not sc:
                continue

            # Audio output
            if sc.model_turn:
                for part in sc.model_turn.parts:
                    if part.inline_data and isinstance(part.inline_data.data, bytes):
                        audio_queue_output.put_nowait(part.inline_data.data)

            # Output transcription (Gemini speaking)
            if sc.output_transcription and sc.output_transcription.text:
                t = sc.output_transcription.text
                gemini_buf += t
                print(t, end="", flush=True)
                if ui:
                    ui.set_status("Gemini speaking…", "#34d399")
                    ui.set_dot("#34d399")

            # Input transcription (user speaking)
            if sc.input_transcription and sc.input_transcription.text:
                t = sc.input_transcription.text
                you_buf += t
                print(f"\033[3m{t}\033[0m", end="", flush=True)
                if ui:
                    ui.set_status("Listening…", "#60a5fa")
                    ui.set_dot("#3b82f6")

            # Turn complete — flush buffers to UI
            if sc.generation_complete:
                print()
                if gemini_buf.strip() and ui:
                    ui.add_message("gemini", gemini_buf.strip())
                    ui.set_status("Ready — speak anytime", "#666")
                    ui.set_dot("#22c55e")
                gemini_buf = ""

            if sc.interrupted:
                # Clear audio queue on barge-in
                while not audio_queue_output.empty():
                    try: audio_queue_output.get_nowait()
                    except: break
                if you_buf.strip() and ui:
                    ui.add_message("you", you_buf.strip())
                you_buf = ""

        # Flush any remaining you_buf after turn ends
        if you_buf.strip() and ui:
            ui.add_message("you", you_buf.strip())
        you_buf = ""


# ─────────────────────────────────────────────────────────────────────────────
# MAIN SESSION
# ─────────────────────────────────────────────────────────────────────────────
async def run_session():
    global hotkey_queue
    hotkey_queue = asyncio.Queue()

    if ui:
        ui.set_status("Connecting to Gemini…", "#f59e0b")
        ui.set_dot("#f59e0b")
        ui.add_message("system", "Connecting to Gemini Live…")

    try:
        async with client.aio.live.connect(model=MODEL, config=CONFIG) as session:
            print("Connected to Gemini. Start speaking!")

            if ui:
                ui.set_status("Ready — speak anytime", "#666")
                ui.set_dot("#22c55e")
                ui.add_message("system", "Connected ✅  Talk naturally or press Ctrl+Space")
                ui.set_snap_callback(
                    lambda: asyncio.get_event_loop().call_soon_threadsafe(
                        hotkey_queue.put_nowait, "trigger"
                    )
                )

            async with asyncio.TaskGroup() as tg:
                tg.create_task(send_audio(session))
                tg.create_task(listen_audio())
                tg.create_task(receive_responses(session))
                tg.create_task(play_audio())
                tg.create_task(send_screen(session))
                tg.create_task(hotkey_loop(session))

    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Session error: {e}")
        import traceback; traceback.print_exc()
        if ui:
            ui.add_message("system", f"Error: {e}")
    finally:
        if audio_stream_in:
            audio_stream_in.close()
        pya.terminate()
        print("\nConnection closed.")
        if ui:
            ui.set_status("Disconnected", "#ef4444")
            ui.set_dot("#ef4444")
            ui.add_message("system", "Session ended.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    global ui

    ui = TutorUI()

    loop      = asyncio.new_event_loop()
    main_task = None

    def shutdown_now():
        _shutdown.set()
        if main_task and not main_task.done():
            loop.call_soon_threadsafe(main_task.cancel)
        ui.quit()

    ui.set_shutdown_callback(shutdown_now)

    # Hotkey
    def _on_hotkey():
        if hotkey_queue is not None and not _shutdown.is_set():
            loop.call_soon_threadsafe(hotkey_queue.put_nowait, "trigger")

    keyboard.add_hotkey("ctrl+space", _on_hotkey, suppress=True)

    # Ctrl+C
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, lambda s, f: (shutdown_now(), print("\nCtrl+C — shutting down…")))

    # Async thread
    def run_async():
        nonlocal main_task
        asyncio.set_event_loop(loop)
        try:
            main_task = loop.create_task(run_session())
            loop.run_until_complete(main_task)
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        except Exception as e:
            import traceback
            print(f"Async error: {e}"); traceback.print_exc()
        finally:
            try: ui.root.after(0, ui.root.quit)
            except Exception: pass

    t = threading.Thread(target=run_async, daemon=True, name="AsyncLoop")
    t.start()

    # Start pulsing dot
    ui.animate_listening()

    # Tk mainloop
    try:
        ui.mainloop()
    finally:
        _shutdown.set()
        keyboard.remove_all_hotkeys()
        if not loop.is_closed():
            loop.call_soon_threadsafe(loop.stop)
        t.join(timeout=5)
        if not loop.is_closed():
            try: loop.close()
            except Exception: pass
        signal.signal(signal.SIGINT, original_sigint)
        print("Goodbye!")


if __name__ == "__main__":
    main()