import mss
import mss.tools
import keyboard
import time
import base64
import json
import ctypes
import math
import tkinter as tk
from anthropic import Anthropic

# 1. We swapped Desktop for Application to allow direct HWND hooking
from pywinauto import Application 

# ---------------------------------------------------------
# DPI AWARENESS FIX
# ---------------------------------------------------------
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass

client = Anthropic(api_key="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")

# Initialize master hidden window for Tkinter to prevent crashes
root = tk.Tk()
root.withdraw() 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# ---------------------------------------------------------
# THE MAGIC: OS-Level Coordinate Snapping (HWND Version)
# ---------------------------------------------------------
def snap_to_element(rough_x, rough_y, target_label, max_distance=300):
    print(f"🔍 UIA Scanner: Searching for an element labeled '{target_label}' near {rough_x}, {rough_y}...")
    
    try:
        # 1. Grab the exact Windows ID (HWND) of the currently active window
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        
        # 2. Force pywinauto to connect ONLY to that specific window ID
        app = Application(backend="uia").connect(handle=hwnd)
        active_window = app.window(handle=hwnd)
        
        best_match = None
        shortest_dist = float('inf')
        
        # 3. Scan the elements inside that specific window
        print("⏳ Scanning UI tree... (Browsers can take a few seconds)")
        for elem in active_window.descendants():
            text = elem.window_text()
            
            # If the element has text and matches what Claude told us to look for
            if text and target_label.lower() in text.lower():
                rect = elem.rectangle()
                mid_x, mid_y = rect.mid_point().x, rect.mid_point().y
                
                # Calculate how far this real element is from Claude's guess
                dist = math.hypot(mid_x - rough_x, mid_y - rough_y)
                
                # If it's the closest one we've found within our search radius, save it!
                if dist < shortest_dist and dist <= max_distance:
                    shortest_dist = dist
                    best_match = (mid_x, mid_y)
                    
        if best_match:
            print(f"✅ UIA Match Found! Adjusted Claude's guess from ({rough_x}, {rough_y}) -> Exact Center: ({best_match[0]}, {best_match[1]})")
            return best_match[0], best_match[1]
        else:
            print(f"⚠️ Could not find exact UIA element for '{target_label}'. Falling back to AI's rough guess.")
            return rough_x, rough_y
            
    except Exception as e:
        print(f"⚠️ UIA Error: {e}")
        return rough_x, rough_y

# ---------------------------------------------------------
# THE OVERLAY (Fake Cursor)
# ---------------------------------------------------------
def draw_ai_pointer(target_x, target_y):
    print("✨ Drawing AI Overlay...")
    
    # Create temporary transparent window
    overlay = tk.Toplevel(root)
    overlay.attributes('-transparentcolor', 'magenta')
    overlay.attributes('-topmost', True)
    overlay.overrideredirect(True)
    overlay.geometry(f"{screen_width}x{screen_height}+0+0")
    
    # Make it click-through so the user can still use their mouse
    hwnd = ctypes.windll.user32.GetParent(overlay.winfo_id())
    styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles | 0x00080000 | 0x00000020)

    canvas = tk.Canvas(overlay, bg='magenta', highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    # Start cursor at the bottom middle of the screen
    start_x, start_y = screen_width // 2, screen_height - 100

    cursor = canvas.create_oval(start_x-8, start_y-8, start_x+8, start_y+8, fill='#007AFF', outline='white', width=2)
    ring = canvas.create_oval(start_x-20, start_y-20, start_x+20, start_y+20, outline='#007AFF', width=3)

    # Animation Math
    steps = 45
    for i in range(steps + 1):
        t = i / steps
        ease_t = t * (2 - t) # Smooth ease-out
        
        curr_x = start_x + (target_x - start_x) * ease_t
        curr_y = start_y + (target_y - start_y) * ease_t
        
        canvas.coords(cursor, curr_x-8, curr_y-8, curr_x+8, curr_y+8)
        canvas.coords(ring, curr_x-20, curr_y-20, curr_x+20, curr_y+20)
        overlay.update()
        time.sleep(0.015)

    # Double pulse animation at destination
    for _ in range(2):
        canvas.coords(ring, target_x-35, target_y-35, target_x+35, target_y+35)
        overlay.update()
        time.sleep(0.15)
        canvas.coords(ring, target_x-20, target_y-20, target_x+20, target_y+20)
        overlay.update()
        time.sleep(0.15)

    time.sleep(1.5)
    overlay.destroy()


def take_screenshot_and_ask_claude():
    print("📸 Snapping screen...")
    with mss.mss() as sct:
        monitor = sct.monitors[1] 
        output = "screen.png"
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    print("🧠 Sending screen to Claude...")
    base64_image = encode_image(output)
    
    system_prompt = f"""You are an AI software tutor. 
    The user's screen resolution is {screen_width}x{screen_height}.
    Find the most important "Primary Action" button on the screen to get started (like "New File", "Blank document", "+", etc).
    
    IMPORTANT: You must provide the EXACT text label written on or near the button so my system can find it in the UI tree. If it is an icon, guess the tooltip text.
    
    Respond ONLY with a raw JSON object using this exact structure:
    {{
        "label": "Blank document",
        "rough_x": 250,
        "rough_y": 380,
        "speech": "I see you have Google Docs open. Click the Blank Document button to start."
    }}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": base64_image}},
                        {"type": "text", "text": system_prompt}
                    ],
                }
            ],
        )
        
        result_text = response.content[0].text
        if "```" in result_text:
            result_text = result_text.split("```")[1].replace("json", "").strip()
            
        data = json.loads(result_text)
        print(f"🗣️ AI Says: {data['speech']}")
        
        # 🚀 Pass Claude's guess into our Windows UIA Scanner!
        exact_x, exact_y = snap_to_element(data["rough_x"], data["rough_y"], data["label"])
        
        draw_ai_pointer(exact_x, exact_y)
        
    except Exception as e:
        print(f"❌ Error: {e}")

print("🤖 HWND-Hooking Tutor running! Press 'Ctrl + Space' to trigger. Press 'Esc' to quit.")

while True:
    if keyboard.is_pressed('ctrl+space'):
        take_screenshot_and_ask_claude()
        time.sleep(2) # Prevent double trigger
    
    # Keep Tkinter master window alive
    root.update()
    time.sleep(0.01)

    if keyboard.is_pressed('esc'):
        print("Shutting down...")
        break