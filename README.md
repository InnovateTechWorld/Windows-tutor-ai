# Windows Tutor AI

I wanted to build a desktop AI tutor that feels less like a terminal chatbot and more like having a smart assistant sitting next to me while I work in Windows. This project listens to what I say, watches the screen, and helps me navigate apps and system workflows with live voice guidance and visual context.

It is built around Google Gemini Live and is designed to do a few things well:

- listen to my voice in real time,
- capture what is happening on screen,
- understand the context of the task,
- answer questions conversationally,
- highlight UI elements and guide me toward the right place.

This is not just an AI chat box running in a terminal. It is a multimodal desktop assistant meant to feel like a live digital coach for Windows users.

---

## Why I built it

Most AI tools are text-first or web-first. I wanted something that actually fits into a real desktop workflow.

The idea is simple:

- the assistant sees the screen,
- listens to the user,
- understands the current context,
- responds with practical help instead of vague text.

That makes it useful for a lot of everyday scenarios:

- onboarding to a new app,
- explaining a workflow step by step,
- helping with Windows programs,
- assisting with system tasks,
- acting like a visual tutor for desktop work.

This project is a hands-on example of applied AI engineering: streaming audio, live screen capture, multimodal reasoning, and desktop automation in one system.

---

## What it does

This app can:

- stream microphone audio into a Gemini Live session,
- capture screenshots continuously,
- interpret what is on-screen in context,
- answer questions in a natural conversational way,
- draw a pointer to important UI elements,
- guide the user toward the right action in the interface.

It is a small but useful prototype for building real-time AI support into a desktop workflow.

---

## Features

- Real-time voice interaction with Gemini Live
- Continuous screen capture using MSS
- Multimodal AI conversation with live visual context
- Conversational desktop tutor with voice responses
- Keyboard-triggered snapshot mode using Ctrl + Space
- Windows UIA element detection and target snapping
- Animated on-screen pointer overlay for visual guidance
- Tkinter-based desktop dashboard with transcript and status
- Automatic speech detection via the Live API configuration
- Support for tool-driven UI guidance

---

## High-level architecture

The project is made up of a few clear moving parts:

1. Audio input pipeline
   - The microphone captures PCM audio.
   - The audio is streamed into the Gemini Live session.
   - The system is designed to support natural conversation.

2. Screen capture pipeline
   - The app captures desktop frames as JPEG images.
   - Those frames are sent to the model as visual context.
   - The model can react to what it sees on the screen.

3. Live AI reasoning layer
   - Gemini Live receives multimodal input in real time.
   - It uses voice and screen context to answer questions and guide the user.
   - The assistant is prompted to act like a helpful tutor.

4. Tool-calling layer
   - The model can request a tool such as point_to_element().
   - The tool identifies a likely UI target using Windows UIA.
   - An animated pointer is drawn to guide the user visually.

5. Desktop UI layer
   - Tkinter provides the interface.
   - The UI shows transcript history and live status.
   - It can also show a small screen preview panel.

This structure keeps the app easy to reason about and easier to improve over time.

---

## Tech stack

- Python
- Google Gemini Live API
- PyAudio
- MSS
- Pillow
- Tkinter
- pywinauto
- keyboard
- python-dotenv
- Windows-specific UI automation

---

## Repository structure

```text
Windows-tutor-ai/
├── tutor.py                     # Earlier Anthropic-based prototype
├── tutor_live.py                # Main Gemini Live Windows tutor
├── workin-code-tutor-gemini.py # Gemini Live implementation with UI
├── find_mic.py                  # Microphone discovery/debug utility
├── gemini_audio_test.py         # Audio test script
├── mic_debug.py                 # Microphone debugging helper
├── gemini-live-doc.md           # Reference notes for Gemini Live
├── screen.png                   # Example captured screenshot
├── .gitignore
├── .ENV                        # Local environment file (not typically committed)
├── README.md
└── LICENSE
```

---

## Getting started

### Prerequisites

This project is built for Windows.

You will need:

- Python 3.10+
- A working microphone and speakers
- A valid Google Gemini API key
- A Windows desktop environment

### Install dependencies

```bash
pip install google-genai pyaudio mss pywinauto pillow keyboard python-dotenv
```

### Configure environment

Create a `.ENV` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

> The app loads this file with python-dotenv and uses it at runtime.

---

## Running the app

From the repository root:

```bash
python tutor_live.py
```

Or, depending on the version you want to use:

```bash
python workin-code-tutor-gemini.py
```

---

## Controls

- Talk naturally to the assistant
- Ctrl + Space: trigger a screen description snapshot
- Ctrl + C: quit
- Close the app window: shutdown the session

The goal is for it to feel responsive and live, so the user can just speak while the AI watches the screen and responds naturally.

---

## How it works

### 1. Capture audio
The app opens the default microphone and streams raw PCM audio chunks to the Gemini Live session.

### 2. Capture screen
Using MSS, it grabs the desktop and converts it into JPEG frames that the model can interpret visually.

### 3. Send multimodal input
The system sends:

- live microphone audio,
- live screenshot frames,
- contextual instructions.

### 4. Receive responses
Gemini streams back:

- spoken audio,
- transcriptions,
- structured tool calls.

### 5. Trigger UI guidance
When the model decides the user needs help, it can call a tool like point_to_element(), which:

- searches Windows UI elements,
- finds the best likely target,
- draws an animated blue pointer to guide the user.

That makes the assistant much more useful than a normal chatbot because it can actively help the user navigate the right area.

---

## Why this is interesting

I think this project is a strong example of practical AI product design. It combines multiple systems into one working experience:

- multimodal AI interaction,
- streaming data pipelines,
- desktop automation,
- real-time UX design,
- tool-based reasoning,
- event-driven orchestration.

The real value is that it turns AI into something useful in the middle of a real user workflow instead of leaving it contained inside a prompt window.

---

## Design strengths

- Practical and user-focused
- Real-time interaction model
- Voice + vision integration
- Windows environment awareness
- Clear separation between runtime components
- Tool-based interaction improves reliability and actionability
- UI designed for low-friction use

---

## Possible next steps

This is already a solid prototype, and it could grow into a stronger product with improvements like:

- better error handling and reconnect logic,
- support for multiple monitors,
- configurable assistant personality and tone,
- richer tool ecosystem,
- system prompts for domain-specific tutoring,
- user profiles and memory,
- logging and session analytics,
- packaging into a Windows installer,
- safer handling of secrets and environment configuration.

---

## Summary

Windows Tutor AI is a practical multimodal assistant that brings AI directly into a desktop workflow. It combines live voice, screen understanding, and Windows UI guidance into a single experience that feels more like a digital coach than a traditional chatbot.

It is a good example of:

- modern AI product thinking,
- multimodal system design,
- real-time application engineering,
- human-centered software experiences.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Note

This repository is a prototype and experimentation space for building a real-time AI desktop tutor. It is best suited for Windows environments and is designed as a hands-on example of multimodal AI in a real desktop context.
