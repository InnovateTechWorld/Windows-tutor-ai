"""
Windows Tutor AI — Gemini Live Edition
=======================================
Based on Google's official working example + screen sharing + Tkinter UI
+ Windows UIA element snapping + animated pointer overlay + tool calling.

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
from datetime import datetime
from pathlib import Path

import keyboard
import mss
import pyaudio
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image, ImageTk
from pywinauto import Application, Desktop

# ─────────────────────────────────────────────────────────────────────────────
# LOAD ENV
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv(Path(__file__).parent / ".ENV")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .ENV file")

client = genai.Client(api_key=GEMINI_API_KEY)

# ─────────────────────────────────────────────────────────────────────────────
# AUDIO CONFIG  (exactly as Google's working example — do not change)
# ─────────────────────────────────────────────────────────────────────────────
FORMAT           = pyaudio.paInt16
CHANNELS         = 1
SEND_SAMPLE_RATE = 16000
RECV_SAMPLE_RATE = 24000
CHUNK_SIZE       = 1024

pya = pyaudio.PyAudio()

# ─────────────────────────────────────────────────────────────────────────────
# GEMINI CONFIG
# ─────────────────────────────────────────────────────────────────────────────
MODEL = "gemini-3.1-flash-live-preview"

SCREEN_W = ctypes.windll.user32.GetSystemMetrics(0)
SCREEN_H = ctypes.windll.user32.GetSystemMetrics(1)

SYSTEM_INSTRUCTION = f"""You are an AI tutor and assistant running on a Windows PC.
Screen resolution: {SCREEN_W}x{SCREEN_H}.
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

POINTING TOOL:
When you want to direct the user's attention to a specific UI element on screen,
call point_to_element() with the exact label text visible on or near that element
and your best estimate of its pixel coordinates.
This will show an animated blue dot that flies across the screen to that element.
Use this whenever you say things like "click here", "look at this button",
"go to this menu", etc. — always point rather than just describe.

Start by greeting the user warmly and briefly describing what you see on their screen."""

# ── Tool declaration ──────────────────────────────────────────────────────────
POINT_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="point_to_element",
            description=(
                "Show an animated pointer on the user's screen to highlight a UI element. "
                "Use this whenever directing the user to click, look at, or interact with "
                "any specific button, menu, link, or UI element."
            ),
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "label": types.Schema(
                        type=types.Type.STRING,
                        description="The exact visible text label on or near the element.",
                    ),
                    "rough_x": types.Schema(
                        type=types.Type.INTEGER,
                        description="Best estimate of element X pixel coordinate on screen.",
                    ),
                    "rough_y": types.Schema(
                        type=types.Type.INTEGER,
                        description="Best estimate of element Y pixel coordinate on screen.",
                    ),
                },
                required=["label", "rough_x", "rough_y"],
            ),
        )
    ]
)

CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[POINT_TOOL],
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
# WINDOWS UIA SNAPPING
# ─────────────────────────────────────────────────────────────────────────────
UIA_MAX_DISTANCE = 400

def snap_to_element(rough_x, rough_y, target_label, max_distance=UIA_MAX_DISTANCE):
    """Search ALL visible windows on desktop for the element — not just foreground."""
    print(f"[UIA] Searching all windows for '{target_label}' near ({rough_x},{rough_y})")
    best, best_dist = None, float("inf")

    try:
        desktop = Desktop(backend="uia")
        # Search every top-level window
        for win in desktop.windows():
            try:
                for elem in win.descendants():
                    try:
                        text = elem.window_text()
                        if not text:
                            continue
                        # Fuzzy match — any word from label found in element text
                        label_words = [w for w in target_label.lower().split() if len(w) > 2]
                        elem_text   = text.lower()
                        if not any(w in elem_text for w in label_words):
                            continue
                        r  = elem.rectangle()
                        mx = r.mid_point().x
                        my = r.mid_point().y
                        # Must be on screen
                        if mx < 0 or my < 0 or mx > SCREEN_W or my > SCREEN_H:
                            continue
                        d = math.hypot(mx - rough_x, my - rough_y)
                        if d < best_dist and d <= max_distance:
                            best_dist, best = d, (mx, my)
                            print(f"[UIA] Candidate: '{text}' at ({mx},{my}) dist={d:.0f}")
                    except Exception:
                        continue
            except Exception:
                continue
    except Exception as e:
        print(f"[UIA] Desktop scan error: {e}")

    if best:
        print(f"[UIA] Best match → ({best[0]},{best[1]}) dist={best_dist:.0f}")
        return best

    print(f"[UIA] No match found, using Gemini's rough coords ({rough_x},{rough_y})")
    return rough_x, rough_y

# ─────────────────────────────────────────────────────────────────────────────
# ANIMATED OVERLAY POINTER
# ─────────────────────────────────────────────────────────────────────────────
def draw_ai_pointer(root, tx, ty):
    """Animate a blue dot flying from bottom-centre to the target element."""
    print(f"[pointer] → ({tx},{ty})")
    ov = tk.Toplevel(root)
    ov.attributes("-transparentcolor", "magenta")
    ov.attributes("-topmost", True)
    ov.overrideredirect(True)
    ov.geometry(f"{SCREEN_W}x{SCREEN_H}+0+0")

    # Make click-through so it doesn't block interaction
    hwnd   = ctypes.windll.user32.GetParent(ov.winfo_id())
    styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles | 0x00080000 | 0x00000020)

    cv = tk.Canvas(ov, bg="magenta", highlightthickness=0)
    cv.pack(fill="both", expand=True)

    sx, sy = SCREEN_W // 2, SCREEN_H - 80
    dot  = cv.create_oval(sx-10, sy-10, sx+10, sy+10,
                           fill="#007AFF", outline="white", width=2)
    ring = cv.create_oval(sx-22, sy-22, sx+22, sy+22,
                           outline="#007AFF", width=3)
    # Label
    lbl = cv.create_text(sx, sy - 30, text="", fill="#ffffff",
                          font=("Segoe UI", 10, "bold"))

    # Fly animation
    for i in range(46):
        t = i / 45
        e = t * (2 - t)          # ease-out
        cx = sx + (tx - sx) * e
        cy = sy + (ty - sy) * e
        cv.coords(dot,  cx-10, cy-10, cx+10, cy+10)
        cv.coords(ring, cx-22, cy-22, cx+22, cy+22)
        ov.update()
        time.sleep(0.012)

    # Pulse at destination
    cv.itemconfig(lbl, text="👆")
    cv.coords(lbl, tx, ty - 36)
    for _ in range(3):
        cv.coords(ring, tx-36, ty-36, tx+36, ty+36)
        ov.update(); time.sleep(0.12)
        cv.coords(ring, tx-22, ty-22, tx+22, ty+22)
        ov.update(); time.sleep(0.12)

    time.sleep(1.2)
    ov.destroy()

# ─────────────────────────────────────────────────────────────────────────────
# TOOL HANDLER
# ─────────────────────────────────────────────────────────────────────────────
def handle_point_to_element(root, label, rough_x, rough_y):
    """Run UIA snap + animated pointer. Called from async via executor."""
    result = {}
    ev     = threading.Event()

    def _run():
        try:
            ex, ey = snap_to_element(rough_x, rough_y, label)
            draw_ai_pointer(root, ex, ey)
            result.update({"status": "success", "exact_x": ex, "exact_y": ey})
        except Exception as e:
            result.update({"status": "error", "error": str(e)})
        finally:
            ev.set()

    root.after(0, _run)
    ev.wait(timeout=30)
    return result

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

        self.always_on_top = tk.BooleanVar(value=True)
        self.root.attributes("-topmost", True)

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._shutdown_callback = None
        self._snap_callback     = None

    def set_shutdown_callback(self, cb): self._shutdown_callback = cb
    def set_snap_callback(self, cb):     self._snap_callback = cb

    def _on_close(self):
        if self._shutdown_callback:
            self._shutdown_callback()
        try: self.root.destroy()
        except Exception: pass

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg="#0f0f0f", pady=16)
        header.pack(fill="x", padx=20)

        title_row = tk.Frame(header, bg="#0f0f0f")
        title_row.pack(fill="x")

        self.status_dot = tk.Canvas(title_row, width=12, height=12,
                                     bg="#0f0f0f", highlightthickness=0)
        self.status_dot.pack(side="left", padx=(0, 8))
        self._dot_oval = self.status_dot.create_oval(2, 2, 10, 10,
                                                      fill="#333", outline="")

        tk.Label(title_row, text="Windows Tutor AI",
                 font=("Segoe UI", 15, "bold"),
                 fg="#ffffff", bg="#0f0f0f").pack(side="left")

        self._status_str = tk.StringVar(value="Connecting…")
        tk.Label(header, textvariable=self._status_str,
                 font=("Segoe UI", 9), fg="#666", bg="#0f0f0f"
                 ).pack(anchor="w", pady=(4, 0))

        tk.Frame(self.root, bg="#1e1e1e", height=1).pack(fill="x", padx=20)

        # ── Transcript ───────────────────────────────────────────────────────
        tf = tk.Frame(self.root, bg="#0f0f0f")
        tf.pack(fill="both", expand=True, padx=12, pady=10)

        self.transcript = tk.Text(
            tf, wrap="word", font=("Segoe UI", 10),
            bg="#111111", fg="#e0e0e0",
            insertbackground="#fff", relief="flat",
            padx=12, pady=10, state="disabled", cursor="arrow",
        )
        self.transcript.pack(fill="both", expand=True)

        self.transcript.tag_configure("you",         foreground="#60a5fa", font=("Segoe UI", 10, "bold"))
        self.transcript.tag_configure("gemini",      foreground="#34d399", font=("Segoe UI", 10, "bold"))
        self.transcript.tag_configure("you_text",    foreground="#bfdbfe")
        self.transcript.tag_configure("gemini_text", foreground="#a7f3d0")
        self.transcript.tag_configure("tool",        foreground="#f59e0b", font=("Segoe UI", 9, "italic"))
        self.transcript.tag_configure("system",      foreground="#555",    font=("Segoe UI", 9, "italic"))

        sb = tk.Scrollbar(tf, command=self.transcript.yview,
                          bg="#1e1e1e", troughcolor="#111", width=6)
        self.transcript.configure(yscrollcommand=sb.set)

        tk.Frame(self.root, bg="#1e1e1e", height=1).pack(fill="x", padx=20)

        # ── Controls ─────────────────────────────────────────────────────────
        ctrl = tk.Frame(self.root, bg="#0f0f0f", pady=14)
        ctrl.pack(fill="x", padx=20)

        self.show_preview = tk.BooleanVar(value=False)
        tk.Checkbutton(ctrl, text="Screen preview",
                       variable=self.show_preview,
                       command=self._toggle_preview,
                       bg="#0f0f0f", fg="#888", activebackground="#0f0f0f",
                       activeforeground="#fff", selectcolor="#1a1a1a",
                       font=("Segoe UI", 9)).pack(side="left")

        tk.Checkbutton(ctrl, text="Always on top",
                       variable=self.always_on_top,
                       command=lambda: self.root.attributes("-topmost", self.always_on_top.get()),
                       bg="#0f0f0f", fg="#888", activebackground="#0f0f0f",
                       activeforeground="#fff", selectcolor="#1a1a1a",
                       font=("Segoe UI", 9)).pack(side="left", padx=(12, 0))

        tk.Button(ctrl, text="⌨  Describe Screen",
                  command=lambda: self._snap_callback() if self._snap_callback else None,
                  bg="#1a1a1a", fg="#888",
                  activebackground="#222", activeforeground="#fff",
                  relief="flat", font=("Segoe UI", 9),
                  padx=10, pady=4).pack(side="right")

        # ── Preview panel (hidden by default) ────────────────────────────────
        self.preview_frame = tk.Frame(self.root, bg="#0f0f0f")
        self.preview_label = tk.Label(self.preview_frame, bg="#111", relief="flat")
        self.preview_label.pack(padx=8, pady=8)

        # ── Footer ────────────────────────────────────────────────────────────
        footer = tk.Frame(self.root, bg="#0a0a0a", pady=8)
        footer.pack(fill="x", side="bottom")
        tk.Label(footer,
                 text="Ctrl+Space = describe screen  •  Ctrl+C = quit",
                 font=("Segoe UI", 8), fg="#333", bg="#0a0a0a").pack()

    def _toggle_preview(self):
        if self.show_preview.get():
            self.preview_frame.pack(fill="x", padx=12,
                                    before=self.root.winfo_children()[-1])
        else:
            self.preview_frame.pack_forget()

    # ── Public API ────────────────────────────────────────────────────────────
    def set_status(self, text, color="#666"):
        self.root.after(0, lambda: self._status_str.set(text))

    def set_dot(self, color):
        self.root.after(0, lambda: self.status_dot.itemconfig(self._dot_oval, fill=color))

    def add_message(self, speaker, text):
        def _do():
            self.transcript.configure(state="normal")
            if speaker == "you":
                self.transcript.insert("end", "You\n", "you")
                self.transcript.insert("end", text + "\n\n", "you_text")
            elif speaker == "gemini":
                self.transcript.insert("end", "Gemini\n", "gemini")
                self.transcript.insert("end", text + "\n\n", "gemini_text")
            elif speaker == "tool":
                self.transcript.insert("end", text + "\n", "tool")
            else:
                self.transcript.insert("end", text + "\n", "system")
            self.transcript.configure(state="disabled")
            self.transcript.see("end")
        self.root.after(0, _do)

    def update_preview(self, jpeg_bytes):
        if not self.show_preview.get():
            return
        def _do():
            try:
                img = Image.open(io.BytesIO(jpeg_bytes))
                img.thumbnail((380, 220), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.preview_label.configure(image=photo)
                self.preview_label._photo = photo
            except Exception:
                pass
        self.root.after(0, _do)

    def animate_listening(self):
        self._pulse(0)

    def _pulse(self, n):
        if not _shutdown.is_set():
            self.set_dot("#22c55e" if n % 2 == 0 else "#166534")
            self.root.after(700, lambda: self._pulse(n + 1))

    def mainloop(self): self.root.mainloop()
    def quit(self):
        try: self.root.quit()
        except Exception: pass


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
# AUDIO TASKS  (Google's working pattern — unchanged)
# ─────────────────────────────────────────────────────────────────────────────
async def listen_audio():
    global audio_stream_in
    mic_info = pya.get_default_input_device_info()
    audio_stream_in = await asyncio.to_thread(
        pya.open,
        format=FORMAT, channels=CHANNELS,
        rate=SEND_SAMPLE_RATE, input=True,
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
        format=FORMAT, channels=CHANNELS,
        rate=RECV_SAMPLE_RATE, output=True,
    )
    while not _shutdown.is_set():
        data = await audio_queue_output.get()
        await asyncio.to_thread(stream.write, data)


# ─────────────────────────────────────────────────────────────────────────────
# SCREEN TASK
# ─────────────────────────────────────────────────────────────────────────────
async def send_screen(session):
    loop = asyncio.get_running_loop()
    while not _shutdown.is_set():
        try:
            jpeg = await loop.run_in_executor(None, capture_screen_jpeg)
            await session.send_realtime_input(
                video=types.Blob(data=jpeg, mime_type="image/jpeg")
            )
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
                ui.add_message("system", "📸 Screen snapshot sent to Gemini")
        except Exception as e:
            print(f"[hotkey] {e}")


# ─────────────────────────────────────────────────────────────────────────────
# RECEIVE TASK  (handles audio + transcripts + tool calls)
# ─────────────────────────────────────────────────────────────────────────────
async def receive_responses(session):
    loop       = asyncio.get_running_loop()
    you_buf    = ""
    gemini_buf = ""

    while not _shutdown.is_set():
        turn = session.receive()
        async for response in turn:
            sc = response.server_content
            if not sc:
                # ── Tool call ────────────────────────────────────────────────
                if response.tool_call:
                    fn_responses = []
                    for fc in response.tool_call.function_calls:
                        print(f"[tool] {fc.name}({fc.args})")
                        if fc.name == "point_to_element":
                            args    = fc.args or {}
                            label   = str(args.get("label", ""))
                            rough_x = int(args.get("rough_x", SCREEN_W // 2))
                            rough_y = int(args.get("rough_y", SCREEN_H // 2))

                            if ui:
                                ui.add_message("tool",
                                    f"👆 Pointing to: {label} ({rough_x},{rough_y})")

                            result = await loop.run_in_executor(
                                None,
                                lambda l=label, x=rough_x, y=rough_y:
                                    handle_point_to_element(ui.root, l, x, y)
                            )
                        else:
                            result = {"error": f"Unknown tool: {fc.name}"}

                        fn_responses.append(
                            types.FunctionResponse(
                                id=fc.id, name=fc.name, response=result
                            )
                        )
                    await session.send_tool_response(function_responses=fn_responses)
                continue

            # ── Audio output ─────────────────────────────────────────────────
            if sc.model_turn:
                for part in sc.model_turn.parts:
                    if part.inline_data and isinstance(part.inline_data.data, bytes):
                        audio_queue_output.put_nowait(part.inline_data.data)

            # ── Gemini speaking transcript ────────────────────────────────────
            if sc.output_transcription and sc.output_transcription.text:
                t = sc.output_transcription.text
                gemini_buf += t
                print(t, end="", flush=True)
                if ui:
                    ui.set_status("Gemini speaking…", "#34d399")
                    ui.set_dot("#34d399")

            # ── User speaking transcript ──────────────────────────────────────
            if sc.input_transcription and sc.input_transcription.text:
                t = sc.input_transcription.text
                you_buf += t
                print(f"\033[3m{t}\033[0m", end="", flush=True)
                if ui:
                    ui.set_status("Listening…", "#60a5fa")
                    ui.set_dot("#3b82f6")

            # ── Turn complete ─────────────────────────────────────────────────
            if sc.generation_complete:
                print()
                if gemini_buf.strip() and ui:
                    ui.add_message("gemini", gemini_buf.strip())
                    ui.set_status("Ready — speak anytime", "#666")
                    ui.set_dot("#22c55e")
                gemini_buf = ""

            # ── Barge-in / interrupted ────────────────────────────────────────
            if sc.interrupted:
                while not audio_queue_output.empty():
                    try: audio_queue_output.get_nowait()
                    except: break
                if you_buf.strip() and ui:
                    ui.add_message("you", you_buf.strip())
                you_buf    = ""
                gemini_buf = ""

        # Flush you_buf after each receive loop iteration
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

                def _snap():
                    loop = asyncio.get_event_loop()
                    loop.call_soon_threadsafe(hotkey_queue.put_nowait, "trigger")

                ui.set_snap_callback(_snap)

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
            ui.add_message("system", f"❌ Error: {e}")
    finally:
        if audio_stream_in:
            try: audio_stream_in.close()
            except Exception: pass
        try: pya.terminate()
        except Exception: pass
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

    ui   = TutorUI()
    loop = asyncio.new_event_loop()
    main_task = None

    def shutdown_now():
        _shutdown.set()
        if main_task and not main_task.done():
            loop.call_soon_threadsafe(main_task.cancel)
        ui.quit()

    ui.set_shutdown_callback(shutdown_now)

    def _on_hotkey():
        if hotkey_queue is not None and not _shutdown.is_set():
            loop.call_soon_threadsafe(hotkey_queue.put_nowait, "trigger")

    keyboard.add_hotkey("ctrl+space", _on_hotkey, suppress=True)

    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT,
                  lambda s, f: (shutdown_now(), print("\nCtrl+C — shutting down…")))

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

    ui.animate_listening()

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