# Windows Tutor AI

A Windows-native, real-time AI tutor that listens to the user, watches the screen, and helps them navigate software with voice guidance and contextual visual understanding.

Built around Google Gemini Live, this project turns the desktop into an intelligent assistant that can:
- hear what the user says,
- capture screenshots continuously,
- understand what is happening on screen,
- answer questions conversationally,
- highlight important UI elements on the desktop,
- guide the user step by step.

This is not just a chatbot running in a terminal. It is a multimodal desktop assistant designed to feel like a live digital coach for Windows users.

---

## Why this project matters

Most AI tools are text-first or web-first. This project takes a different approach: it brings AI directly into the user’s desktop workflow.

The core value is simple but powerful:
- the assistant sees the user’s screen,
- listens to their voice,
- interprets context in real time,
- offers actionable help without forcing the user to describe everything manually.

That makes it especially useful for:
- onboarding new users,
- explaining software workflows,
- helping with Windows applications,
- guiding tasks step-by-step,
- acting like a visual teaching assistant for desktop environments.

This project demonstrates real-world AI engineering in a practical and approachable way: streaming audio, screen capture, live model interaction, tool calling, and Windows automation in one system.

---

## Key features

- Real-time voice interaction with Gemini Live
- Continuous screen capture using MSS
- Multimodal AI conversation with live visual context
- Conversational desktop tutor with voice responses
- Keyboard-triggered snapshot mode using Ctrl + Space
- Windows UIA element detection and target snapping
- Animated on-screen pointer overlay to highlight interface elements
- Tkinter-based desktop dashboard with transcript and status
- Automatic speech detection through the Live API configuration
- Support for tool-driven UI guidance

---

## High-level architecture

This project is a good example of pragmatic AI system design. It combines several subsystems into one live experience:

1. Audio input pipeline
   - The microphone captures PCM audio.
   - The audio is streamed into the Gemini Live session.
   - Voice Activity Detection (VAD) supports natural conversational flow.

2. Screen capture pipeline
   - The app captures desktop frames as JPEG images.
   - These images are sent to the model as visual context.
   - The model can respond to what it sees on the screen.

3. Live AI reasoning layer
   - Gemini Live receives multimodal input in real time.
   - The model uses voice + image context to answer and guide.
   - The system prompts the assistant to behave like a helpful tutor.

4. Tool-calling layer
   - The model can request a tool like point_to_element().
   - The tool identifies the likely UI target using Windows UIA.
   - A pointer animation is drawn to visually guide the user.

5. Desktop UI layer
   - Tkinter provides a minimal but polished interface.
   - The UI displays transcript history and system states.
   - It optionally shows a small screen preview panel.

This architecture is strong because it separates concerns cleanly:
- input capture,
- model communication,
- UI interaction,
- Windows automation,
- visual guidance.

That is exactly the kind of structure that makes an AI product easier to debug, extend, and improve over time.

---

## Tech stack

- Python
- Google Gemini Live API
- PyAudio
- MSS (screen capture)
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
└── .ENV                        # Local environment file (not committed in many setups)
```

---

## Getting started

### Prerequisites

This project is designed for Windows.

You will need:
- Python 3.10+
- A working microphone and speakers
- A valid Google Gemini API key
- Windows desktop environment

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

or, depending on the version you want to use:

```bash
python workin-code-tutor-gemini.py
```

---

## Controls

- Talk naturally to the assistant
- Ctrl + Space: trigger a screen description snapshot
- Ctrl + C: quit
- Close the app window: shutdown the session

The app is designed to feel live and responsive, so the user can simply speak while the AI watches the screen and responds naturally.

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
- contextual textual instructions.

### 4. Receive responses
Gemini streams back:
- spoken audio,
- transcriptions,
- structured tool calls.

### 5. Trigger UI guidance
When the model decides the user needs help, it can call a tool such as point_to_element(), which:
- searches Windows UI elements,
- finds the best likely target,
- draws an animated blue pointer to guide the user.

This makes the assistant feel much more useful than a normal chatbot because it can actively direct the user to the right place.

---

## Why the engineering is strong

This project is a solid example of applied AI engineering because it blends multiple systems into a cohesive product:

- multimodal AI interaction,
- streaming data pipelines,
- desktop automation,
- real-time UX design,
- tool-based reasoning,
- event-driven orchestration.

From an engineering perspective, the app is valuable because it solves an important product problem:
translating AI capabilities into a helpful live experience on a real user desktop.

It is not merely a demo script; it shows how to build a system where:
- the AI understands context,
- the application responds in real time,
- the user receives visual and conversational feedback,
- the system can take action beyond text alone.

---

## Design strengths

- Practical and user-centric
- Real-time interaction model
- Voice + vision integration
- Windows environment awareness
- Clear separation between core runtime components
- Tool-based interaction improves reliability and actionability
- UI designed for immediate, low-friction use

---

## Considerations and next steps

This is an excellent prototype, and it can grow into a more robust product with improvements like:

- better error handling and reconnect logic,
- support for multiple monitors,
- configurable assistant personality and tone,
- richer tool ecosystem,
- system prompts for domain-specific tutoring,
- user profiles and context memory,
- logging and session analytics,
- packaging into an executable installer for Windows,
- safer handling of environment and secrets.

---

## Summary

Windows Tutor AI is a practical, well-architected multimodal assistant that brings AI directly into a desktop workflow. It combines live voice, screen understanding, and Windows UI guidance into an experience that feels like a digital tutor walking beside the user.

It is a compelling example of:
- modern AI product thinking,
- multimodal system design,
- real-time application engineering,
- human-centered software experiences.

---

## License

This project currently does not declare a license. Add a license if you plan to share or distribute it publicly.

## Note

This repository is a prototype and experimentation space for building a real-time AI desktop tutor. It is best suited for Windows environments and is designed as a hands-on example of multimodal AI application development.
