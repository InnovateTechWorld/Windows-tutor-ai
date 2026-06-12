The Live API enables low-latency, real-time voice and vision interactions with
Gemini. It processes continuous streams of audio, images, and text to deliver
immediate, human-like spoken responses, creating a natural conversational
experience for your users.

![Live API Overview](https://ai.google.dev/static/gemini-api/docs/images/live-api-overview.png)
[Try the Live API in Google AI Studio](https://aistudio.google.com/live) [Clone example apps from GitHub](https://github.com/google-gemini/gemini-live-api-examples) [Use coding agent skills](https://ai.google.dev/gemini-api/docs/coding-agents)

## Use cases

Live API can be used to build real-time voice agents for a
variety of industries, including:

- **E-commerce and retail:** Shopping assistants that offer personalized recommendations and support agents that resolve customer issues.
- **Gaming:** Interactive non-player characters (NPCs), in-game help assistants, and real-time translation of in-game content.
- **Next-gen interfaces:** Voice- and video-enabled experiences in robotics, smart glasses, and vehicles.
- **Healthcare:** Health companions for patient support and education.
- **Financial services:** AI advisors for wealth management and investment guidance.
- **Education:** AI mentors and learner companions that provide personalized instruction and feedback.

## Key features

Live API offers a comprehensive set of features for building
robust voice agents:

- [**Multilingual support**](https://ai.google.dev/gemini-api/docs/live-guide#supported-languages): Converse in 70 supported languages.
- [**Barge-in**](https://ai.google.dev/gemini-api/docs/live-guide#interruptions): Users can interrupt the model at any time for responsive interactions.
- [**Tool use**](https://ai.google.dev/gemini-api/docs/live-tools): Integrates tools like function calling and Google Search for dynamic interactions.
- [**Audio transcriptions**](https://ai.google.dev/gemini-api/docs/live-guide#audio-transcription): Provides text transcripts of both user input and model output.
- [**Proactive audio**](https://ai.google.dev/gemini-api/docs/live-guide#proactive-audio): Lets you control when the model responds and in what contexts.
- [**Affective dialog**](https://ai.google.dev/gemini-api/docs/live-guide#affective-dialog): Adapts response style and tone to match the user's input expression.

## Technical specifications

The following table outlines the technical specifications for the
Live API:

| Category | Details |
|---|---|
| Input modalities | Audio (raw 16-bit PCM audio, 16kHz, little-endian), images (JPEG \<= 1FPS), text |
| Output modalities | Audio (raw 16-bit PCM audio, 24kHz, little-endian) |
| Protocol | Stateful WebSocket connection (WSS) |

## Choose an implementation approach

When integrating with Live API, you'll need to choose one of the following
implementation approaches:

- **Server-to-server** : Your backend connects to the Live API using [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API). Typically, your client sends stream data (audio, video, text) to your server, which then forwards it to the Live API.
- **Client-to-server** : Your frontend code connects directly to the Live API using [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to stream data, bypassing your backend.

> [!NOTE]
> **Note:** Client-to-server generally offers better performance for streaming audio and video, since it bypasses the need to send the stream to your backend first. It's also easier to set up since you don't need to implement a proxy that sends data from your client to your server and then your server to the API. However, for production environments, in order to mitigate security risks, we recommend using [ephemeral tokens](https://ai.google.dev/gemini-api/docs/ephemeral-tokens) instead of standard API keys.

## Get started

Select the guide that matches your development environment:
Server-to-server

### [GenAI SDK tutorial](https://ai.google.dev/gemini-api/docs/live-api/get-started-sdk)


Connect to the Gemini Live API using the GenAI SDK to build a real-time multimodal application with a Python backend.

Client-to-server

### [WebSocket tutorial](https://ai.google.dev/gemini-api/docs/live-api/get-started-websocket)


Connect to the Gemini Live API using WebSockets to build a real-time multimodal application with a JavaScript frontend and ephemeral tokens.

Agent development kit

### [ADK tutorial](https://google.github.io/adk-docs/streaming/)


Create an agent and use the Agent Development Kit (ADK) Streaming to enable voice and video communication.

## Partner integrations


To streamline the development of real-time audio and video apps, you can use
a third-party integration that supports the Gemini Live
API over WebRTC or WebSockets.
[LiveKit
Use the Gemini Live API with LiveKit Agents.](https://docs.livekit.io/agents/models/realtime/plugins/gemini/) [Pipecat by Daily
Create a real-time AI chatbot using Gemini Live and Pipecat.](https://docs.pipecat.ai/guides/features/gemini-live) [Fishjam by Software Mansion
Create live video and audio streaming applications with Fishjam.](https://docs.fishjam.io/tutorials/gemini-live-integration) [Vision Agents by Stream
Build real-time voice and video AI applications with Vision Agents.](https://visionagents.ai/integrations/gemini) [Voximplant
Connect inbound and outbound calls to Live API with Voximplant.](https://voximplant.com/products/gemini-client) [Agora
Build real-time conversational AI applications with Agora.](https://docs.agora.io/en/conversational-ai/models/mllm/gemini) [Firebase AI SDK
Get started with the Gemini Live API using Firebase AI Logic.](https://firebase.google.com/docs/ai-logic/live-api?api=dev)




The Gemini Live API allows for real-time, bidirectional interaction with Gemini models, supporting audio, video, and text inputs and native audio outputs. This guide explains how to integrate with the API using the Google GenAI SDK on your server.
[Try the Live API in Google AI Studio](https://aistudio.google.com/live) [Clone the example app from GitHub](https://github.com/google-gemini/gemini-live-api-examples/tree/main/gemini-live-genai-python-sdk) [Use coding agent skills](https://ai.google.dev/gemini-api/docs/coding-agents)

## Overview

The Gemini Live API uses WebSockets for real-time communication. The `google-genai` SDK provides a high-level asynchronous interface for managing these connections.

Key concepts:

- **Session**: A persistent connection to the model.
- **Config**: Setting up modalities (audio/text), voice, and system instructions.
- **Real-time Input**: Sending audio and video frames as blobs.

## Connecting to the Live API

Start a Live API session with an API key:

### Python

    import asyncio
    from google import genai

    client = genai.Client(api_key="YOUR_API_KEY")

    model = "gemini-3.1-flash-live-preview"
    config = {"response_modalities": ["AUDIO"]}

    async def main():
        async with client.aio.live.connect(model=model, config=config) as session:
            print("Session started")
            # Send content...

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    import { GoogleGenAI, Modality } from '@google/genai';

    const ai = new GoogleGenAI({ apiKey: "YOUR_API_KEY"});
    const model = 'gemini-3.1-flash-live-preview';
    const config = { responseModalities: [Modality.AUDIO] };

    async function main() {

      const session = await ai.live.connect({
        model: model,
        callbacks: {
          onopen: function () {
            console.debug('Opened');
          },
          onmessage: function (message) {
            console.debug(message);
          },
          onerror: function (e) {
            console.debug('Error:', e.message);
          },
          onclose: function (e) {
            console.debug('Close:', e.reason);
          },
        },
        config: config,
      });

      console.debug("Session started");
      // Send content...

      session.close();
    }

    main();

## Sending text

Text can be sent using `send_realtime_input` (Python) or `sendRealtimeInput` (JavaScript).

### Python

    await session.send_realtime_input(text="Hello, how are you?")

### JavaScript

    session.sendRealtimeInput({
      text: 'Hello, how are you?'
    });

## Sending audio

Audio needs to be sent as raw PCM data (raw 16-bit PCM audio, 16kHz, little-endian).

### Python

    # Assuming 'chunk' is your raw PCM audio bytes
    await session.send_realtime_input(
        audio=types.Blob(
            data=chunk,
            mime_type="audio/pcm;rate=16000"
        )
    )

### JavaScript

    // Assuming 'chunk' is a Buffer of raw PCM audio
    session.sendRealtimeInput({
      audio: {
        data: chunk.toString('base64'),
        mimeType: 'audio/pcm;rate=16000'
      }
    });

For an example of how to get the audio from the client device (e.g. the browser)
see the end-to-end example on [GitHub](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-genai-python-sdk/frontend/media-handler.js#L31-L70).

## Sending video

Video frames are sent as individual images (e.g., JPEG or PNG) at a specific frame rate (max 1 frame per second).

### Python

    # Assuming 'frame' is your JPEG-encoded image bytes
    await session.send_realtime_input(
        video=types.Blob(
            data=frame,
            mime_type="image/jpeg"
        )
    )

### JavaScript

    // Assuming 'frame' is a Buffer of JPEG-encoded image data
    session.sendRealtimeInput({
      video: {
        data: frame.toString('base64'),
        mimeType: 'image/jpeg'
      }
    });

For an example of how to get the video from the client device (e.g. the browser)
see the end-to-end example on [GitHub](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-genai-python-sdk/frontend/media-handler.js#L84-L120).

## Receiving audio

The model's audio responses are received as chunks of data.

### Python

    async for response in session.receive():
        if response.server_content and response.server_content.model_turn:
            for part in response.server_content.model_turn.parts:
                if part.inline_data:
                    audio_data = part.inline_data.data
                    # Process or play the audio data

### JavaScript

    // Inside the onmessage callback
    const content = response.serverContent;
    if (content?.modelTurn?.parts) {
      for (const part of content.modelTurn.parts) {
        if (part.inlineData) {
          const audioData = part.inlineData.data;
          // Process or play audioData (base64 encoded string)
        }
      }
    }

See the example app on GitHub to learn how to [receive the audio on your server](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-genai-python-sdk/gemini_live.py#L86-L98) and [play it in the browser](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-genai-python-sdk/frontend/media-handler.js#L145-L174).

## Receiving text

Transcriptions for both user input and model output are available in the server content.

### Python

    async for response in session.receive():
        content = response.server_content
        if content:
            if content.input_transcription:
                print(f"User: {content.input_transcription.text}")
            if content.output_transcription:
                print(f"Gemini: {content.output_transcription.text}")

### JavaScript

    // Inside the onmessage callback
    const content = response.serverContent;
    if (content?.inputTranscription) {
      console.log('User:', content.inputTranscription.text);
    }
    if (content?.outputTranscription) {
      console.log('Gemini:', content.outputTranscription.text);
    }

## Handling tool calls

The API supports tool calling (function calling). When the model requests a tool call, you must execute the function and send the response back.

### Python

    async for response in session.receive():
        if response.tool_call:
            function_responses = []
            for fc in response.tool_call.function_calls:
                # 1. Execute the function locally
                result = my_tool_function(**fc.args)

                # 2. Prepare the response
                function_responses.append(types.FunctionResponse(
                    name=fc.name,
                    id=fc.id,
                    response={"result": result}
                ))

            # 3. Send the tool response back to the session
            await session.send_tool_response(function_responses=function_responses)

### JavaScript

    // Inside the onmessage callback
    if (response.toolCall) {
      const functionResponses = [];
      for (const fc of response.toolCall.functionCalls) {
        const result = myToolFunction(fc.args);
        functionResponses.push({
          name: fc.name,
          id: fc.id,
          response: { result }
        });
      }
      session.sendToolResponse({ functionResponses });
    }

## What's next

- Read the full Live API [Capabilities](https://ai.google.dev/gemini-api/docs/live-guide) guide for key capabilities and configurations; including Voice Activity Detection and native audio features.
- Read the [Tool use](https://ai.google.dev/gemini-api/docs/live-tools) guide to learn how to integrate Live API with tools and function calling.
- Read the [Session management](https://ai.google.dev/gemini-api/docs/live-session) guide for managing long running conversations.
- Read the [Ephemeral tokens](https://ai.google.dev/gemini-api/docs/ephemeral-tokens) guide for secure authentication in [client-to-server](https://ai.google.dev/gemini-api/docs/live-api/get-started-sdk#implementation-approach) applications.
- For more information about the underlying WebSockets API, see the [WebSockets API reference](https://ai.google.dev/api/live).


The Gemini Live API allows for real-time, bidirectional interaction with Gemini models, supporting audio, video, and text inputs and native audio outputs. This guide explains how to integrate directly with the API using raw WebSockets.
[Try the Live API in Google AI Studio](https://aistudio.google.com/live) [Clone the example app from GitHub](https://github.com/google-gemini/gemini-live-api-examples/tree/main/gemini-live-ephemeral-tokens-websocket) [Use coding agent skills](https://ai.google.dev/gemini-api/docs/coding-agents)

## Overview

The Gemini Live API uses WebSockets for real-time communication. Unlike using an SDK, this approach involves directly managing the WebSocket connection and sending/receiving messages in a specific JSON format defined by the API.

Key concepts:

- **WebSocket Endpoint**: The specific URL to connect to.
- **Message Format** : All communication is done via JSON messages conforming to [`BidiGenerateContentClientMessage`](https://ai.google.dev/api/live#bidigeneratecontentclientmessage) and [`BidiGenerateContentServerMessage`](https://ai.google.dev/api/live#bidigeneratecontentservermessage) structures.
- **Session Management**: You are responsible for maintaining the WebSocket connection.

## Authentication

Authentication is handled by including your API key as a query parameter in the WebSocket URL.

The endpoint format is:

    wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key=YOUR_API_KEY

Replace `YOUR_API_KEY` with your actual API key.

## Authentication with Ephemeral Tokens

If you are using [ephemeral tokens](https://ai.google.dev/gemini-api/docs/ephemeral-tokens), you need to connect to the `v1alpha` endpoint.
The ephemeral token needs to be passed as an `access_token` query parameter.

The endpoint format for ephemeral keys is:

    wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContentConstrained?access_token={short-lived-token}

Replace `{short-lived-token}` with the actual ephemeral token.

## Connecting to the Live API

To start a live session, establish a WebSocket connection to the authenticated endpoint.
The first message sent over the WebSocket must be a [`BidiGenerateContentSetup`](https://ai.google.dev/api/live#bidigeneratecontentsetup) containing the `config`.
For the full configuration options, see the [Live API - WebSockets API reference](https://ai.google.dev/api/live).

### Python

    import asyncio
    import websockets
    import json

    API_KEY = "YOUR_API_KEY"
    MODEL_NAME = "gemini-3.1-flash-live-preview"
    WS_URL = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key={API_KEY}"

    async def connect_and_configure():
        async with websockets.connect(WS_URL) as websocket:
            print("WebSocket Connected")

            # 1. Send the initial configuration
            config_message = {
                "config": {
                    "model": f"models/{MODEL_NAME}",
                    "responseModalities": ["AUDIO"],
                    "systemInstruction": {
                        "parts": [{"text": "You are a helpful assistant."}]
                    }
                }
            }
            await websocket.send(json.dumps(config_message))
            print("Configuration sent")

            # Keep the session alive for further interactions
            await asyncio.sleep(3600) # Example: keep open for an hour

    async def main():
        await connect_and_configure()

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    const API_KEY = "YOUR_API_KEY";
    const MODEL_NAME = "gemini-3.1-flash-live-preview";
    const WS_URL = `wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key=${API_KEY}`;

    const websocket = new WebSocket(WS_URL);

    websocket.onopen = () => {
      console.log('WebSocket Connected');

      // 1. Send the initial configuration
      const configMessage = {
        config: {
          model: `models/${MODEL_NAME}`,
          responseModalities: ['AUDIO'],
          systemInstruction: {
            parts: [{ text: 'You are a helpful assistant.' }]
          }
        }
      };
      websocket.send(JSON.stringify(configMessage));
      console.log('Configuration sent');
    };

    websocket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      console.log('Received:', response);
      // Handle different types of responses here
    };

    websocket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket Closed');
    };

## Sending text

To send text input, construct a [`BidiGenerateContentRealtimeInput`](https://ai.google.dev/api/live#bidigeneratecontentrealtimeinput) message with the `text` field.

### Python

    # Inside the websocket context
    async def send_text(websocket, text):
        text_message = {
            "realtimeInput": {
                "text": text
            }
        }
        await websocket.send(json.dumps(text_message))
        print(f"Sent text: {text}")

    # Example usage: await send_text(websocket, "Hello, how are you?")

### JavaScript

    function sendTextMessage(text) {
      if (websocket.readyState === WebSocket.OPEN) {
        const textMessage = {
          realtimeInput: {
            text: text
          }
        };
        websocket.send(JSON.stringify(textMessage));
        console.log('Text message sent:', text);
      } else {
        console.warn('WebSocket not open.');
      }
    }

    // Example usage:
    sendTextMessage("Hello, how are you?");

## Sending audio

Audio needs to be sent as raw PCM data (raw 16-bit PCM audio, 16kHz, little-endian). Construct a [`BidiGenerateContentRealtimeInput`](https://ai.google.dev/api/live#bidigeneratecontentrealtimeinput) message with the audio data. The `mimeType` is crucial.

### Python

    # Inside the websocket context
    async def send_audio_chunk(websocket, chunk_bytes):
        import base64
        encoded_data = base64.b64encode(chunk_bytes).decode('utf-8')
        audio_message = {
            "realtimeInput": {
                "audio": {
                    "data": encoded_data,
                    "mimeType": "audio/pcm;rate=16000"
                }
            }
        }
        await websocket.send(json.dumps(audio_message))
        # print("Sent audio chunk") # Avoid excessive logging

    # Assuming 'chunk' is your raw PCM audio bytes
    # await send_audio_chunk(websocket, chunk)

### JavaScript

    // Assuming 'chunk' is a Buffer of raw PCM audio
    function sendAudioChunk(chunk) {
      if (websocket.readyState === WebSocket.OPEN) {
        const audioMessage = {
          realtimeInput: {
            audio: {
              data: chunk.toString('base64'),
              mimeType: 'audio/pcm;rate=16000'
            }
          }
        };
        websocket.send(JSON.stringify(audioMessage));
        // console.log('Sent audio chunk');
      }
    }
    // Example usage: sendAudioChunk(audioBuffer);

For an example of how to get the audio from the client device (e.g. the browser)
see the end-to-end example on [GitHub](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-ephemeral-tokens-websocket/frontend/mediaUtils.js#L38-L74).

## Sending video

Video frames are sent as individual images (e.g., JPEG or PNG). Similar to audio, use `realtimeInput` with a `Blob`, specifying the correct `mimeType`.

### Python

    # Inside the websocket context
    async def send_video_frame(websocket, frame_bytes, mime_type="image/jpeg"):
        import base64
        encoded_data = base64.b64encode(frame_bytes).decode('utf-8')
        video_message = {
            "realtimeInput": {
                "video": {
                    "data": encoded_data,
                    "mimeType": mime_type
                }
            }
        }
        await websocket.send(json.dumps(video_message))
        # print("Sent video frame")

    # Assuming 'frame' is your JPEG-encoded image bytes
    # await send_video_frame(websocket, frame)

### JavaScript

    // Assuming 'frame' is a Buffer of JPEG-encoded image data
    function sendVideoFrame(frame, mimeType = 'image/jpeg') {
      if (websocket.readyState === WebSocket.OPEN) {
        const videoMessage = {
          realtimeInput: {
            video: {
              data: frame.toString('base64'),
              mimeType: mimeType
            }
          }
        };
        websocket.send(JSON.stringify(videoMessage));
        // console.log('Sent video frame');
      }
    }
    // Example usage: sendVideoFrame(jpegBuffer);

For an example of how to get the video from the client device (e.g. the browser)
see the end-to-end example on [GitHub](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-ephemeral-tokens-websocket/frontend/mediaUtils.js#L185-L222).

## Receiving responses

The WebSocket will send back [`BidiGenerateContentServerMessage`](https://ai.google.dev/api/live#bidigeneratecontentservermessage) messages. You need to parse these JSON messages and handle different types of content.

### Python

    # Inside the websocket context, in a receive loop
    async def receive_loop(websocket):
        async for message in websocket:
            response = json.loads(message)
            print("Received:", response)

            if "serverContent" in response:
                server_content = response["serverContent"]
                # Receiving Audio
                if "modelTurn" in server_content and "parts" in server_content["modelTurn"]:
                    for part in server_content["modelTurn"]["parts"]:
                        if "inlineData" in part:
                            audio_data_b64 = part["inlineData"]["data"]
                            # Process or play the base64 encoded audio data
                            # audio_data = base64.b64decode(audio_data_b64)
                            print(f"Received audio data (base64 len: {len(audio_data_b64)})")

                # Receiving Text Transcriptions
                if "inputTranscription" in server_content:
                    print(f"User: {server_content['inputTranscription']['text']}")
                if "outputTranscription" in server_content:
                    print(f"Gemini: {server_content['outputTranscription']['text']}")

            # Handling Tool Calls
            if "toolCall" in response:
                await handle_tool_call(websocket, response["toolCall"])

    # Example usage: await receive_loop(websocket)

### JavaScript

    websocket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      console.log('Received:', response);

      if (response.serverContent) {
        const serverContent = response.serverContent;
        // Receiving Audio
        if (serverContent.modelTurn?.parts) {
          for (const part of serverContent.modelTurn.parts) {
            if (part.inlineData) {
              const audioData = part.inlineData.data; // Base64 encoded string
              // Process or play audioData
              console.log(`Received audio data (base64 len: ${audioData.length})`);
            }
          }
        }

        // Receiving Text Transcriptions
        if (serverContent.inputTranscription) {
          console.log('User:', serverContent.inputTranscription.text);
        }
        if (serverContent.outputTranscription) {
          console.log('Gemini:', serverContent.outputTranscription.text);
        }
      }

      // Handling Tool Calls
      if (response.toolCall) {
        handleToolCall(response.toolCall);
      }
    };

For an example of how to handle the response, see the end-to-end example on [GitHub](https://github.com/google-gemini/gemini-live-api-examples/blob/main/gemini-live-ephemeral-tokens-websocket/frontend/geminilive.js#L22-L75).

## Handling tool calls

When the model requests a tool call, the [`BidiGenerateContentServerMessage`](https://ai.google.dev/api/live#bidigeneratecontentservermessage) will contain a `toolCall` field. You must execute the function locally and send the result back to the WebSocket using a [`BidiGenerateContentToolResponse`](https://ai.google.dev/api/live#bidigeneratecontenttoolresponse) message.

### Python

    # Placeholder for your tool function
    def my_tool_function(args):
        print(f"Executing tool with args: {args}")
        # Implement your tool logic here
        return {"status": "success", "data": "some result"}

    async def handle_tool_call(websocket, tool_call):
        function_responses = []
        for fc in tool_call["functionCalls"]:
            # 1. Execute the function locally
            try:
                result = my_tool_function(fc.get("args", {}))
                response_data = {"result": result}
            except Exception as e:
                print(f"Error executing tool {fc['name']}: {e}")
                response_data = {"error": str(e)}

            # 2. Prepare the response
            function_responses.append({
                "name": fc["name"],
                "id": fc["id"],
                "response": response_data
            })

        # 3. Send the tool response back to the session
        tool_response_message = {
            "toolResponse": {
                "functionResponses": function_responses
            }
        }
        await websocket.send(json.dumps(tool_response_message))
        print("Sent tool response")

    # This function is called within the receive_loop when a toolCall is detected.

### JavaScript

    // Placeholder for your tool function
    function myToolFunction(args) {
      console.log(`Executing tool with args:`, args);
      // Implement your tool logic here
      return { status: 'success', data: 'some result' };
    }

    function handleToolCall(toolCall) {
      const functionResponses = [];
      for (const fc of toolCall.functionCalls) {
        // 1. Execute the function locally
        let result;
        try {
          result = myToolFunction(fc.args || {});
        } catch (e) {
          console.error(`Error executing tool ${fc.name}:`, e);
          result = { error: e.message };
        }

        // 2. Prepare the response
        functionResponses.push({
          name: fc.name,
          id: fc.id,
          response: { result }
        });
      }

      // 3. Send the tool response back to the session
      if (websocket.readyState === WebSocket.OPEN) {
        const toolResponseMessage = {
          toolResponse: {
            functionResponses: functionResponses
          }
        };
        websocket.send(JSON.stringify(toolResponseMessage));
        console.log('Sent tool response');
      } else {
        console.warn('WebSocket not open to send tool response.');
      }
    }
    // This function is called within websocket.onmessage when a toolCall is detected.

## What's next

- Read the full Live API [Capabilities](https://ai.google.dev/gemini-api/docs/live-guide) guide for key capabilities and configurations; including Voice Activity Detection and native audio features.
- Read the [Tool use](https://ai.google.dev/gemini-api/docs/live-tools) guide to learn how to integrate Live API with tools and function calling.
- Read the [Session management](https://ai.google.dev/gemini-api/docs/live-session) guide for managing long running conversations.
- Read the [Ephemeral tokens](https://ai.google.dev/gemini-api/docs/ephemeral-tokens) guide for secure authentication in [client-to-server](https://ai.google.dev/gemini-api/docs/live-api/get-started-websocket#implementation-approach) applications.
- For more information about the underlying WebSockets API, see the [WebSockets API reference](https://ai.google.dev/api/live).


> [!WARNING]
> **Preview:** The Live API is in preview.

This is a comprehensive guide that covers capabilities and configurations
available with the Live API.
See [Get started with Live API](https://ai.google.dev/gemini-api/docs/live) page for an
overview and sample code for common use cases.

## Before you begin

- **Familiarize yourself with core concepts:** If you haven't already done so, read the [Get started with Live API](https://ai.google.dev/gemini-api/docs/live) page first. This will introduce you to the fundamental principles of the Live API, how it works, and the different [implementation approaches](https://ai.google.dev/gemini-api/docs/live#implementation-approach).
- **Try the Live API in AI Studio:** You may find it useful to try the Live API in [Google AI Studio](https://aistudio.google.com/app/live) before you start building. To use the Live API in Google AI Studio, select **Stream**.

## Model comparison

The following table summarizes the key differences between the
[Gemini 3.1 Flash Live Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-live-preview) and the [Gemini 2.5 Flash Live Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-native-audio-preview-12-2025) models:

| Feature | Gemini 3.1 Flash Live Preview | Gemini 2.5 Flash Live Preview |
|---|---|---|
| **[Thinking](https://ai.google.dev/gemini-api/docs/live-api/capabilities#native-audio-output-thinking)** | Uses `thinkingLevel` to control thinking depth with settings like `minimal`, `low`, `medium`, and `high`. Defaults to `minimal` to optimize for lowest latency. See [Thinking levels and budgets](https://ai.google.dev/gemini-api/docs/thinking#levels-budgets). | Uses `thinkingBudget` to set the number of thinking tokens. Dynamic thinking is enabled by default. Set `thinkingBudget` to `0` to disable. See [Thinking levels and budgets](https://ai.google.dev/gemini-api/docs/thinking#levels-budgets). |
| **[Receiving response](https://ai.google.dev/api/live#bidigeneratecontentservercontent)** | A single server event can contain multiple content parts simultaneously (for example, `inlineData` and transcript). Ensure your code processes all parts in each event to avoid missing content. | Each server event contains only one content part. Parts are delivered in separate events. |
| **[Client content](https://ai.google.dev/gemini-api/docs/live-api/capabilities#incremental-updates)** | `send_client_content` is only supported for seeding initial context history (requires setting `initial_history_in_client_content` in session config). To send text updates during the conversation, use `send_realtime_input` instead. | `send_client_content` is supported throughout the conversation for sending incremental content updates and establishing context. |
| **[Turn coverage](https://ai.google.dev/api/live#turncoverage)** | Defaults to `TURN_INCLUDES_AUDIO_ACTIVITY_AND_ALL_VIDEO`. The model's turn includes detected audio activity and all video frames. | Defaults to `TURN_INCLUDES_ONLY_ACTIVITY`. The model's turn includes only the detected activity. |
| **[Custom VAD](https://ai.google.dev/gemini-api/docs/live-api/capabilities#disable-automatic-vad)** (`activity_start`/`activity_end`) | Supported. Disable automatic VAD and send `activityStart` and `activityEnd` messages manually to control turn boundaries. | Supported. Disable automatic VAD and send `activityStart` and `activityEnd` messages manually to control turn boundaries. |
| **[Automatic VAD configuration](https://ai.google.dev/gemini-api/docs/live-api/capabilities#configure-automatic-vad)** | Supported. Configure parameters such as `start_of_speech_sensitivity`, `end_of_speech_sensitivity`, `prefix_padding_ms`, and `silence_duration_ms`. | Supported. Configure parameters such as `start_of_speech_sensitivity`, `end_of_speech_sensitivity`, `prefix_padding_ms`, and `silence_duration_ms`. |
| **[Asynchronous function calling](https://ai.google.dev/gemini-api/docs/live-tools#async-function-calling)** (`behavior: NON_BLOCKING`) | Not supported. Function calling is sequential only. The model will not start responding until you've sent the tool response. | Supported. Set `behavior` to `NON_BLOCKING` on a function declaration to let the model continue interacting while the function runs. Control how the model handles responses with the `scheduling` parameter (`INTERRUPT`, `WHEN_IDLE`, or `SILENT`). |
| **[Proactive audio](https://ai.google.dev/gemini-api/docs/live-api/capabilities#proactive-audio)** | Not supported | Supported. When enabled, the model can proactively decide not to respond if the input content is not relevant. Set `proactive_audio` to `true` in the `proactivity` config (requires `v1alpha`). |
| **[Affective dialogue](https://ai.google.dev/gemini-api/docs/live-api/capabilities#affective-dialog)** | Not supported | Supported. The model adapts its response style to match the expression and tone of the input. Set `enable_affective_dialog` to `true` in session config (requires `v1alpha`). |

To migrate from Gemini 2.5 Flash Live to Gemini 3.1 Flash Live, see the [migration guide](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-live-preview#migrating).

## Establishing a connection

The following example shows how to create a connection with an API key:

### Python

    import asyncio
    from google import genai

    client = genai.Client()

    model = "gemini-3.1-flash-live-preview"
    config = {"response_modalities": ["AUDIO"]}

    async def main():
        async with client.aio.live.connect(model=model, config=config) as session:
            print("Session started")
            # Send content...

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    import { GoogleGenAI, Modality } from '@google/genai';

    const ai = new GoogleGenAI({});
    const model = 'gemini-3.1-flash-live-preview';
    const config = { responseModalities: [Modality.AUDIO] };

    async function main() {

      const session = await ai.live.connect({
        model: model,
        callbacks: {
          onopen: function () {
            console.debug('Opened');
          },
          onmessage: function (message) {
            console.debug(message);
          },
          onerror: function (e) {
            console.debug('Error:', e.message);
          },
          onclose: function (e) {
            console.debug('Close:', e.reason);
          },
        },
        config: config,
      });

      console.debug("Session started");
      // Send content...

      session.close();
    }

    main();

## Interaction modalities

The following sections provide examples and supporting context for the different
input and output modalities available in Live API.

### Sending audio

Audio needs to be sent as raw PCM data (raw 16-bit PCM audio, 16kHz, little-endian).

### Python

    # Assuming 'chunk' is your raw PCM audio bytes
    await session.send_realtime_input(
        audio=types.Blob(
            data=chunk,
            mime_type="audio/pcm;rate=16000"
        )
    )

### JavaScript

    // Assuming 'chunk' is a Buffer of raw PCM audio
    session.sendRealtimeInput({
      audio: {
        data: chunk.toString('base64'),
        mimeType: 'audio/pcm;rate=16000'
      }
    });

### Audio formats

Audio data in the Live API is always raw, little-endian,
16-bit PCM. Audio output always uses a sample rate of 24kHz. Input audio
is natively 16kHz, but the Live API will resample if needed
so any sample rate can be sent. To convey the sample rate of input audio, set
the MIME type of each audio-containing [Blob](https://ai.google.dev/api/caching#Blob) to a value
like `audio/pcm;rate=16000`.

### Receiving audio

The model's audio responses are received as chunks of data.

### Python

    async for response in session.receive():
        if response.server_content and response.server_content.model_turn:
            for part in response.server_content.model_turn.parts:
                if part.inline_data:
                    audio_data = part.inline_data.data
                    # Process or play the audio data

### JavaScript

    // Inside the onmessage callback
    const content = response.serverContent;
    if (content?.modelTurn?.parts) {
      for (const part of content.modelTurn.parts) {
        if (part.inlineData) {
          const audioData = part.inlineData.data;
          // Process or play audioData (base64 encoded string)
        }
      }
    }

### Sending text

Text can be sent using `send_realtime_input` (Python) or `sendRealtimeInput` (JavaScript).

### Python

    await session.send_realtime_input(text="Hello, how are you?")

### JavaScript

    session.sendRealtimeInput({
      text: 'Hello, how are you?'
    });

### Sending video

Video frames are sent as individual images (e.g., JPEG or PNG) at a specific frame rate (max 1 frame per second).

### Python

    # Assuming 'frame' is your JPEG-encoded image bytes
    await session.send_realtime_input(
        video=types.Blob(
            data=frame,
            mime_type="image/jpeg"
        )
    )

### JavaScript

    // Assuming 'frame' is a Buffer of JPEG-encoded image data
    session.sendRealtimeInput({
      video: {
        data: frame.toString('base64'),
        mimeType: 'image/jpeg'
      }
    });

#### Incremental content updates

Use incremental updates to send text input, establish session context, or
restore session context. For short contexts you can send turn-by-turn
interactions to represent the exact sequence of events:

> [!NOTE]
> **Note:** For `gemini-3.1-flash-live-preview`, `send_client_content` is only supported for seeding initial context history. You must set [`initial_history_in_client_content`](https://ai.google.dev/api/live#HistoryConfig) to `true` in the session config's `history_config`. After the first model turn, use `send_realtime_input` with the `text` field instead.

### Python

    turns = [
        {"role": "user", "parts": [{"text": "What is the capital of France?"}]},
        {"role": "model", "parts": [{"text": "Paris"}]},
    ]

    await session.send_client_content(turns=turns, turn_complete=False)

    turns = [{"role": "user", "parts": [{"text": "What is the capital of Germany?"}]}]

    await session.send_client_content(turns=turns, turn_complete=True)

### JavaScript

    let inputTurns = [
      { "role": "user", "parts": [{ "text": "What is the capital of France?" }] },
      { "role": "model", "parts": [{ "text": "Paris" }] },
    ]

    session.sendClientContent({ turns: inputTurns, turnComplete: false })

    inputTurns = [{ "role": "user", "parts": [{ "text": "What is the capital of Germany?" }] }]

    session.sendClientContent({ turns: inputTurns, turnComplete: true })

For longer contexts it's recommended to provide a single message summary to free
up the context window for subsequent interactions. See [Session Resumption](https://ai.google.dev/gemini-api/docs/live-session#session-resumption) for another method for
loading session context.

### Audio transcriptions

In addition to the model response, you can also receive transcriptions of
both the audio output and the audio input.

To enable transcription of the model's audio output, send
`output_audio_transcription` in the setup config. The transcription language is
inferred from the model's response.

### Python

    import asyncio
    from google import genai
    from google.genai import types

    client = genai.Client()
    model = "gemini-3.1-flash-live-preview"

    config = {
        "response_modalities": ["AUDIO"],
        "output_audio_transcription": {}
    }

    async def main():
        async with client.aio.live.connect(model=model, config=config) as session:
            message = "Hello? Gemini are you there?"

            await session.send_client_content(
                turns={"role": "user", "parts": [{"text": message}]}, turn_complete=True
            )

            async for response in session.receive():
                if response.server_content.model_turn:
                    print("Model turn:", response.server_content.model_turn)
                if response.server_content.output_transcription:
                    print("Transcript:", response.server_content.output_transcription.text)

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    import { GoogleGenAI, Modality } from '@google/genai';

    const ai = new GoogleGenAI({});
    const model = 'gemini-3.1-flash-live-preview';

    const config = {
      responseModalities: [Modality.AUDIO],
      outputAudioTranscription: {}
    };

    async function live() {
      const responseQueue = [];

      async function waitMessage() {
        let done = false;
        let message = undefined;
        while (!done) {
          message = responseQueue.shift();
          if (message) {
            done = true;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 100));
          }
        }
        return message;
      }

      async function handleTurn() {
        const turns = [];
        let done = false;
        while (!done) {
          const message = await waitMessage();
          turns.push(message);
          if (message.serverContent && message.serverContent.turnComplete) {
            done = true;
          }
        }
        return turns;
      }

      const session = await ai.live.connect({
        model: model,
        callbacks: {
          onopen: function () {
            console.debug('Opened');
          },
          onmessage: function (message) {
            responseQueue.push(message);
          },
          onerror: function (e) {
            console.debug('Error:', e.message);
          },
          onclose: function (e) {
            console.debug('Close:', e.reason);
          },
        },
        config: config,
      });

      const inputTurns = 'Hello how are you?';
      session.sendClientContent({ turns: inputTurns });

      const turns = await handleTurn();

      for (const turn of turns) {
        if (turn.serverContent && turn.serverContent.outputTranscription) {
          console.debug('Received output transcription: %s\n', turn.serverContent.outputTranscription.text);
        }
      }

      session.close();
    }

    async function main() {
      await live().catch((e) => console.error('got error', e));
    }

    main();

To enable transcription of the model's audio input, send
`input_audio_transcription` in setup config.

### Python

    import asyncio
    from pathlib import Path
    from google import genai
    from google.genai import types

    client = genai.Client()
    model = "gemini-3.1-flash-live-preview"

    config = {
        "response_modalities": ["AUDIO"],
        "input_audio_transcription": {},
    }

    async def main():
        async with client.aio.live.connect(model=model, config=config) as session:
            audio_data = Path("16000.pcm").read_bytes()

            await session.send_realtime_input(
                audio=types.Blob(data=audio_data, mime_type='audio/pcm;rate=16000')
            )

            async for msg in session.receive():
                if msg.server_content.input_transcription:
                    print('Transcript:', msg.server_content.input_transcription.text)

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    import { GoogleGenAI, Modality } from '@google/genai';
    import * as fs from "node:fs";
    import pkg from 'wavefile';
    const { WaveFile } = pkg;

    const ai = new GoogleGenAI({});
    const model = 'gemini-3.1-flash-live-preview';

    const config = {
      responseModalities: [Modality.AUDIO],
      inputAudioTranscription: {}
    };

    async function live() {
      const responseQueue = [];

      async function waitMessage() {
        let done = false;
        let message = undefined;
        while (!done) {
          message = responseQueue.shift();
          if (message) {
            done = true;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 100));
          }
        }
        return message;
      }

      async function handleTurn() {
        const turns = [];
        let done = false;
        while (!done) {
          const message = await waitMessage();
          turns.push(message);
          if (message.serverContent && message.serverContent.turnComplete) {
            done = true;
          }
        }
        return turns;
      }

      const session = await ai.live.connect({
        model: model,
        callbacks: {
          onopen: function () {
            console.debug('Opened');
          },
          onmessage: function (message) {
            responseQueue.push(message);
          },
          onerror: function (e) {
            console.debug('Error:', e.message);
          },
          onclose: function (e) {
            console.debug('Close:', e.reason);
          },
        },
        config: config,
      });

      // Send Audio Chunk
      const fileBuffer = fs.readFileSync("16000.wav");

      // Ensure audio conforms to API requirements (16-bit PCM, 16kHz, mono)
      const wav = new WaveFile();
      wav.fromBuffer(fileBuffer);
      wav.toSampleRate(16000);
      wav.toBitDepth("16");
      const base64Audio = wav.toBase64();

      // If already in correct format, you can use this:
      // const fileBuffer = fs.readFileSync("sample.pcm");
      // const base64Audio = Buffer.from(fileBuffer).toString('base64');

      session.sendRealtimeInput(
        {
          audio: {
            data: base64Audio,
            mimeType: "audio/pcm;rate=16000"
          }
        }
      );

      const turns = await handleTurn();
      for (const turn of turns) {
        if (turn.text) {
          console.debug('Received text: %s\n', turn.text);
        }
        else if (turn.data) {
          console.debug('Received inline data: %s\n', turn.data);
        }
        else if (turn.serverContent && turn.serverContent.inputTranscription) {
          console.debug('Received input transcription: %s\n', turn.serverContent.inputTranscription.text);
        }
      }

      session.close();
    }

    async function main() {
      await live().catch((e) => console.error('got error', e));
    }

    main();

### Change voice and language

[Native audio output](https://ai.google.dev/gemini-api/docs/live-api/capabilities#native-audio-output) models support any of the voices
available for our [Text-to-Speech (TTS)](https://ai.google.dev/gemini-api/docs/speech-generation#voices)
models. You can listen to all the voices in [AI Studio](https://aistudio.google.com/app/live).

To specify a voice, set the voice name within the `speechConfig` object as part
of the session configuration:

### Python

    config = {
        "response_modalities": ["AUDIO"],
        "speech_config": {
            "voice_config": {"prebuilt_voice_config": {"voice_name": "Kore"}}
        },
    }

### JavaScript

    const config = {
      responseModalities: [Modality.AUDIO],
      speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: "Kore" } } }
    };

> [!NOTE]
> **Note:** If you're using the `generateContent` API, the set of available voices is slightly different. See the [speech generation guide](https://ai.google.dev/gemini-api/docs/speech-generation#voices) for `generateContent` audio generation voices.

The Live API supports [multiple languages](https://ai.google.dev/gemini-api/docs/live-api/capabilities#supported-languages).
[Native audio output](https://ai.google.dev/gemini-api/docs/live-api/capabilities#native-audio-output) models automatically choose
the appropriate language and don't support explicitly setting the language
code.

## Native audio capabilities

Our latest models feature [native audio output](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-live-preview),
which provides natural, realistic-sounding speech and improved multilingual
performance.

### Thinking

Gemini 3.1 models use `thinkingLevel` to control thinking depth, with settings
like `minimal`, `low`, `medium`, and `high`. The default is `minimal` to
optimize for lowest latency. Gemini 2.5 models use
`thinkingBudget` to set the number of thinking tokens instead. For more details
on levels vs budgets, see
[Thinking levels and budgets](https://ai.google.dev/gemini-api/docs/thinking#levels-budgets).

### Python

    model = "gemini-3.1-flash-live-preview"

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"]
        thinking_config=types.ThinkingConfig(
            thinking_level="low",
        )
    )

    async with client.aio.live.connect(model=model, config=config) as session:
        # Send audio input and receive audio

### JavaScript

    const model = 'gemini-3.1-flash-live-preview';
    const config = {
      responseModalities: [Modality.AUDIO],
      thinkingConfig: {
        thinkingLevel: 'low',
      },
    };

    async function main() {

      const session = await ai.live.connect({
        model: model,
        config: config,
        callbacks: ...,
      });

      // Send audio input and receive audio

      session.close();
    }

    main();

Additionally, you can enable thought summaries by setting `includeThoughts` to
`true` in your configuration. See [thought summaries](https://ai.google.dev/gemini-api/docs/thinking#summaries)
for more info:

### Python

    model = "gemini-3.1-flash-live-preview"

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"]
        thinking_config=types.ThinkingConfig(
            thinking_level="low",
            include_thoughts=True
        )
    )

### JavaScript

    const model = 'gemini-3.1-flash-live-preview';
    const config = {
      responseModalities: [Modality.AUDIO],
      thinkingConfig: {
        thinkingLevel: 'low',
        includeThoughts: true,
      },
    };

### Affective dialog

This feature lets Gemini adapt its response style to the input expression and
tone.

> [!NOTE]
> **Note:** This feature is not supported in Gemini 3.1 Flash Live.

To use affective dialog, set the api version to `v1alpha` and set
`enable_affective_dialog` to `true`in the setup message:

### Python

    client = genai.Client(http_options={"api_version": "v1alpha"})

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        enable_affective_dialog=True
    )

### JavaScript

    const ai = new GoogleGenAI({ httpOptions: {"apiVersion": "v1alpha"} });

    const config = {
      responseModalities: [Modality.AUDIO],
      enableAffectiveDialog: true
    };

### Proactive audio

When this feature is enabled, Gemini can proactively decide not to respond
if the content is not relevant.

> [!NOTE]
> **Note:** This feature is not supported in Gemini 3.1 Flash Live.

To use it, set the api version to `v1alpha` and configure the `proactivity`
field in the setup message and set `proactive_audio` to `true`:

### Python

    client = genai.Client(http_options={"api_version": "v1alpha"})

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        proactivity={'proactive_audio': True}
    )

### JavaScript

    const ai = new GoogleGenAI({ httpOptions: {"apiVersion": "v1alpha"} });

    const config = {
      responseModalities: [Modality.AUDIO],
      proactivity: { proactiveAudio: true }
    }

## Voice Activity Detection (VAD)

Voice Activity Detection (VAD) allows the model to recognize when a person is
speaking. This is essential for creating natural conversations, as it allows a
user to interrupt the model at any time.

When VAD detects an interruption, the ongoing generation is canceled and
discarded. Only the information already sent to the client is retained in the
session history. The server then sends a [`BidiGenerateContentServerContent`](https://ai.google.dev/api/live#bidigeneratecontentservercontent) message to report the interruption.

The Gemini server then discards any pending function calls and sends a
`BidiGenerateContentServerContent` message with the IDs of the canceled calls.

### Python

    async for response in session.receive():
        if response.server_content.interrupted is True:
            # The generation was interrupted

            # If realtime playback is implemented in your application,
            # you should stop playing audio and clear queued playback here.

### JavaScript

    const turns = await handleTurn();

    for (const turn of turns) {
      if (turn.serverContent && turn.serverContent.interrupted) {
        // The generation was interrupted

        // If realtime playback is implemented in your application,
        // you should stop playing audio and clear queued playback here.
      }
    }

### Automatic VAD

By default, the model automatically performs VAD on
a continuous audio input stream. VAD can be configured with the
[`realtimeInputConfig.automaticActivityDetection`](https://ai.google.dev/api/live#RealtimeInputConfig.AutomaticActivityDetection)
field of the [setup configuration](https://ai.google.dev/api/live#BidiGenerateContentSetup).

When the audio stream is paused for more than a second (for example,
because the user switched off the microphone), an
[`audioStreamEnd`](https://ai.google.dev/api/live#BidiGenerateContentRealtimeInput.FIELDS.bool.BidiGenerateContentRealtimeInput.audio_stream_end)
event should be sent to flush any cached audio. The client can resume sending
audio data at any time.

### Python

    # example audio file to try:
    # URL = "https://storage.googleapis.com/generativeai-downloads/data/hello_are_you_there.pcm"
    # !wget -q $URL -O sample.pcm
    import asyncio
    from pathlib import Path
    from google import genai
    from google.genai import types

    client = genai.Client()
    model = "gemini-3.1-flash-live-preview"

    config = {"response_modalities": ["AUDIO"]}

    async def main():
        async with client.aio.live.connect(model=model, config=config) as session:
            audio_bytes = Path("sample.pcm").read_bytes()

            await session.send_realtime_input(
                audio=types.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
            )

            # if stream gets paused, send:
            # await session.send_realtime_input(audio_stream_end=True)

            async for response in session.receive():
                if response.text is not None:
                    print(response.text)

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    // example audio file to try:
    // URL = "https://storage.googleapis.com/generativeai-downloads/data/hello_are_you_there.pcm"
    // !wget -q $URL -O sample.pcm
    import { GoogleGenAI, Modality } from '@google/genai';
    import * as fs from "node:fs";

    const ai = new GoogleGenAI({});
    const model = 'gemini-3.1-flash-live-preview';
    const config = { responseModalities: [Modality.AUDIO] };

    async function live() {
      const responseQueue = [];

      async function waitMessage() {
        let done = false;
        let message = undefined;
        while (!done) {
          message = responseQueue.shift();
          if (message) {
            done = true;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 100));
          }
        }
        return message;
      }

      async function handleTurn() {
        const turns = [];
        let done = false;
        while (!done) {
          const message = await waitMessage();
          turns.push(message);
          if (message.serverContent && message.serverContent.turnComplete) {
            done = true;
          }
        }
        return turns;
      }

      const session = await ai.live.connect({
        model: model,
        callbacks: {
          onopen: function () {
            console.debug('Opened');
          },
          onmessage: function (message) {
            responseQueue.push(message);
          },
          onerror: function (e) {
            console.debug('Error:', e.message);
          },
          onclose: function (e) {
            console.debug('Close:', e.reason);
          },
        },
        config: config,
      });

      // Send Audio Chunk
      const fileBuffer = fs.readFileSync("sample.pcm");
      const base64Audio = Buffer.from(fileBuffer).toString('base64');

      session.sendRealtimeInput(
        {
          audio: {
            data: base64Audio,
            mimeType: "audio/pcm;rate=16000"
          }
        }

      );

      // if stream gets paused, send:
      // session.sendRealtimeInput({ audioStreamEnd: true })

      const turns = await handleTurn();
      for (const turn of turns) {
        if (turn.text) {
          console.debug('Received text: %s\n', turn.text);
        }
        else if (turn.data) {
          console.debug('Received inline data: %s\n', turn.data);
        }
      }

      session.close();
    }

    async function main() {
      await live().catch((e) => console.error('got error', e));
    }

    main();

With `send_realtime_input`, the API will respond to audio automatically based
on VAD. While `send_client_content` adds messages to the model context in
order, `send_realtime_input` is optimized for responsiveness at the expense of
deterministic ordering.

### Automatic VAD configuration

For more control over the VAD activity, you can configure the following
parameters. See [API reference](https://ai.google.dev/api/live#automaticactivitydetection) for more
info.

### Python

    from google.genai import types

    config = {
        "response_modalities": ["AUDIO"],
        "realtime_input_config": {
            "automatic_activity_detection": {
                "disabled": False, # default
                "start_of_speech_sensitivity": types.StartSensitivity.START_SENSITIVITY_LOW,
                "end_of_speech_sensitivity": types.EndSensitivity.END_SENSITIVITY_LOW,
                "prefix_padding_ms": 20,
                "silence_duration_ms": 100,
            }
        }
    }

### JavaScript

    import { GoogleGenAI, Modality, StartSensitivity, EndSensitivity } from '@google/genai';

    const config = {
      responseModalities: [Modality.AUDIO],
      realtimeInputConfig: {
        automaticActivityDetection: {
          disabled: false, // default
          startOfSpeechSensitivity: StartSensitivity.START_SENSITIVITY_LOW,
          endOfSpeechSensitivity: EndSensitivity.END_SENSITIVITY_LOW,
          prefixPaddingMs: 20,
          silenceDurationMs: 100,
        }
      }
    };

### Disable automatic VAD

Alternatively, the automatic VAD can be disabled by setting
`realtimeInputConfig.automaticActivityDetection.disabled` to `true` in the setup
message. In this configuration the client is responsible for detecting user
speech and sending
[`activityStart`](https://ai.google.dev/api/live#BidiGenerateContentRealtimeInput.FIELDS.BidiGenerateContentRealtimeInput.ActivityStart.BidiGenerateContentRealtimeInput.activity_start)
and [`activityEnd`](https://ai.google.dev/api/live#BidiGenerateContentRealtimeInput.FIELDS.BidiGenerateContentRealtimeInput.ActivityEnd.BidiGenerateContentRealtimeInput.activity_end)
messages at the appropriate times. An `audioStreamEnd` isn't sent in
this configuration. Instead, any interruption of the stream is marked by
an `activityEnd` message.

### Python

    config = {
        "response_modalities": ["AUDIO"],
        "realtime_input_config": {"automatic_activity_detection": {"disabled": True}},
    }

    async with client.aio.live.connect(model=model, config=config) as session:
        # ...
        await session.send_realtime_input(activity_start=types.ActivityStart())
        await session.send_realtime_input(
            audio=types.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
        )
        await session.send_realtime_input(activity_end=types.ActivityEnd())
        # ...

### JavaScript

    const config = {
      responseModalities: [Modality.AUDIO],
      realtimeInputConfig: {
        automaticActivityDetection: {
          disabled: true,
        }
      }
    };

    session.sendRealtimeInput({ activityStart: {} })

    session.sendRealtimeInput(
      {
        audio: {
          data: base64Audio,
          mimeType: "audio/pcm;rate=16000"
        }
      }

    );

    session.sendRealtimeInput({ activityEnd: {} })

### Understanding VAD parameters and their impact on quality

When using automatic VAD, two key parameters control how audio is
segmented into speech turns before being sent to the model:

- **`prefixPaddingMs`** : The amount of audio to include *before* speech is detected. This "look-back" ensures the model captures the full onset of speech, including the first syllable which may start before the VAD triggers. A value of `0` may cause the beginning of words to be clipped.
- **`silenceDurationMs`**: How long the server waits through silence before ending a speech turn. This determines how tolerant the system is of natural mid-sentence pauses (e.g., thinking, breathing, or clause boundaries).

#### Impact of `silenceDurationMs` on audio quality

The `silenceDurationMs` value directly affects the size and completeness
of audio chunks the model receives for processing:

- **Recommended (500ms--800ms):** Provides a good balance---the model receives complete, contextually rich audio chunks while keeping latency reasonable. The server's internal default is approximately 800ms.
- **Too low (e.g., 100ms--200ms):** The system ends speech turns during natural pauses, splitting a single utterance into multiple small audio fragments. The model receives these fragments individually, losing cross-fragment context and resulting in lower transcription and response quality.
- **Too high (e.g., 2000ms+):** The system waits a long time after the user stops speaking, increasing perceived latency before the model responds.

#### Best practices for manual (client-side) VAD

When you disable automatic VAD and manage `activityStart`/`activityEnd`
signals from your own client-side voice detection, be aware that the
server's built-in audio buffering mechanisms are bypassed. This means:

1. **No pre-speech buffer:** The server no longer prepends audio before the detected speech start. Your client should include sufficient audio context before sending `activityStart`.
2. **No silence tolerance:** The server acts immediately on your `activityEnd` signal with no additional wait. If your client-side VAD uses an aggressive end-of-speech threshold (e.g., 200ms of silence), speech may be cut off mid-sentence during natural pauses.

To preserve audio quality with manual VAD, use an end-of-speech silence
threshold of at least **500ms** in your client's voice activity detector.
Thresholds below this value often cause fragmented audio that degrades
transcription and model response quality.

## Token count

You can find the total number of consumed tokens in the
[usageMetadata](https://ai.google.dev/api/live#usagemetadata) field of the returned server message.

### Python

    async for message in session.receive():
        # The server will periodically send messages that include UsageMetadata.
        if message.usage_metadata:
            usage = message.usage_metadata
            print(
                f"Used {usage.total_token_count} tokens in total. Response token breakdown:"
            )
            for detail in usage.response_tokens_details:
                match detail:
                    case types.ModalityTokenCount(modality=modality, token_count=count):
                        print(f"{modality}: {count}")

### JavaScript

    const turns = await handleTurn();

    for (const turn of turns) {
      if (turn.usageMetadata) {
        console.debug('Used %s tokens in total. Response token breakdown:\n', turn.usageMetadata.totalTokenCount);

        for (const detail of turn.usageMetadata.responseTokensDetails) {
          console.debug('%s\n', detail);
        }
      }
    }

## Media resolution

You can specify the media resolution for the input media by setting the
`mediaResolution` field as part of the session configuration:

### Python

    from google.genai import types

    config = {
        "response_modalities": ["AUDIO"],
        "media_resolution": types.MediaResolution.MEDIA_RESOLUTION_LOW,
    }

### JavaScript

    import { GoogleGenAI, Modality, MediaResolution } from '@google/genai';

    const config = {
        responseModalities: [Modality.AUDIO],
        mediaResolution: MediaResolution.MEDIA_RESOLUTION_LOW,
    };

## Limitations

Consider the following limitations of the Live API
when you plan your project.

### Response modalities

The native audio models only support \`AUDIO response modality. If you need the
model response as text, use the [output audio transcription](https://ai.google.dev/gemini-api/docs/live-api/capabilities#audio-transcription)
feature.

### Client authentication

The Live API only provides server-to-server authentication
by default. If you're implementing your Live API application
using a [client-to-server approach](https://ai.google.dev/gemini-api/docs/live#implementation-approach), you need to use
[ephemeral tokens](https://ai.google.dev/gemini-api/docs/ephemeral-tokens) to mitigate security
risks.

### Session duration

Audio-only sessions are limited to 15 minutes,
and audio plus video sessions are limited to 2 minutes.
However, you can configure different [session management techniques](https://ai.google.dev/gemini-api/docs/live-session) for unlimited extensions on session duration.

### Context window

A session has a context window limit of:

- 128k tokens for [native audio output](https://ai.google.dev/gemini-api/docs/live-api/capabilities#native-audio-output) models
- 32k tokens for other Live API models

## Supported languages

Live API supports the following 97 languages.

> [!NOTE]
> **Note:** [Native audio output](https://ai.google.dev/gemini-api/docs/live-api/capabilities#native-audio-output) models can switch between languages naturally during conversation. You can also restrict the languages it speaks in by specifying it in the system instructions.

| Language | BCP-47 Code | Language | BCP-47 Code |
|---|---|---|---|
| Afrikaans | `af` | Latvian | `lv` |
| Akan | `ak` | Lithuanian | `lt` |
| Albanian | `sq` | Macedonian | `mk` |
| Amharic | `am` | Malay | `ms` |
| Arabic | `ar` | Malayalam | `ml` |
| Armenian | `hy` | Maltese | `mt` |
| Assamese | `as` | Maori | `mi` |
| Azerbaijani | `az` | Marathi | `mr` |
| Basque | `eu` | Mongolian | `mn` |
| Belarusian | `be` | Nepali | `ne` |
| Bengali | `bn` | Norwegian | `no` |
| Bosnian | `bs` | Odia | `or` |
| Bulgarian | `bg` | Oromo | `om` |
| Burmese | `my` | Pashto | `ps` |
| Catalan | `ca` | Persian | `fa` |
| Cebuano | `ceb` | Polish | `pl` |
| Chinese | `zh` | Portuguese | `pt` |
| Croatian | `hr` | Punjabi | `pa` |
| Czech | `cs` | Quechua | `qu` |
| Danish | `da` | Romanian | `ro` |
| Dutch | `nl` | Romansh | `rm` |
| English | `en` | Russian | `ru` |
| Estonian | `et` | Serbian | `sr` |
| Faroese | `fo` | Sindhi | `sd` |
| Filipino | `fil` | Sinhala | `si` |
| Finnish | `fi` | Slovak | `sk` |
| French | `fr` | Slovenian | `sl` |
| Galician | `gl` | Somali | `so` |
| Georgian | `ka` | Southern Sotho | `st` |
| German | `de` | Spanish | `es` |
| Greek | `el` | Swahili | `sw` |
| Gujarati | `gu` | Swedish | `sv` |
| Hausa | `ha` | Tajik | `tg` |
| Hebrew | `iw` | Tamil | `ta` |
| Hindi | `hi` | Telugu | `te` |
| Hungarian | `hu` | Thai | `th` |
| Icelandic | `is` | Tswana | `tn` |
| Indonesian | `id` | Turkish | `tr` |
| Irish | `ga` | Turkmen | `tk` |
| Italian | `it` | Ukrainian | `uk` |
| Japanese | `ja` | Urdu | `ur` |
| Kannada | `kn` | Uzbek | `uz` |
| Kazakh | `kk` | Vietnamese | `vi` |
| Khmer | `km` | Welsh | `cy` |
| Kinyarwanda | `rw` | Western Frisian | `fy` |
| Korean | `ko` | Wolof | `wo` |
| Kurdish | `ku` | Yoruba | `yo` |
| Kyrgyz | `ky` | Zulu | `zu` |
| Lao | `lo` |   |   |

## What's next

- Read the [Tool Use](https://ai.google.dev/gemini-api/docs/live-tools) and [Session Management](https://ai.google.dev/gemini-api/docs/live-session) guides for essential information on using the Live API effectively.
- Try the Live API in [Google AI Studio](https://aistudio.google.com/app/live).
- For more info about the Live API models, see [Gemini 2.5 Flash Native Audio](https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-native-audio) on the Models page.
- Try more examples in the [Live API cookbook](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_LiveAPI.ipynb), the [Live API Tools cookbook](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_LiveAPI_tools.ipynb), and the [Live API Get Started script](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_LiveAPI.py).



Tool use allows Live API to go beyond just conversation by enabling it to
perform actions in the real-world and pull in external context while maintaining
a real time connection.
You can define tools such as [Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
and [Google Search](https://ai.google.dev/gemini-api/docs/grounding) with the Live API.

## Overview of supported tools

Here's a brief overview of the available tools for Live API models:

| Tool | Gemini 3.1 Flash Live Preview | Gemini 2.5 Flash Live Preview |
|---|---|---|
| **Search** | Supported | Supported |
| **Function calling** | Supported (synchronous only) | Supported (synchronous and [asynchronous](https://ai.google.dev/gemini-api/docs/live-api/tools#async-function-calling)) |
| **Google Maps** | Not supported | Not supported |
| **Code execution** | Not supported | Not supported |
| **URL context** | Not supported | Not supported |

## Function calling

Live API supports function calling, just like regular content generation
requests. Function calling lets the Live API interact with external data and
programs, greatly increasing what your applications can accomplish.

You can define function declarations as part of the session configuration.
After receiving tool calls, the client should respond with a list of
`FunctionResponse` objects using the `session.send_tool_response` method.

See the [Function calling tutorial](https://ai.google.dev/gemini-api/docs/function-calling) to learn
more.

> [!NOTE]
> **Note:** Unlike the `generateContent` API, the Live API doesn't support automatic tool response handling. You must handle tool responses manually in your client code.

### Python

    import asyncio
    import wave
    from google import genai
    from google.genai import types

    client = genai.Client()

    model = "gemini-3.1-flash-live-preview"

    # Simple function definitions
    turn_on_the_lights = {"name": "turn_on_the_lights"}
    turn_off_the_lights = {"name": "turn_off_the_lights"}

    tools = [{"function_declarations": [turn_on_the_lights, turn_off_the_lights]}]
    config = {"response_modalities": ["AUDIO"], "tools": tools}

    async def main():
        async with client.aio.live.connect(model=model, config=config) as session:
            prompt = "Turn on the lights please"
            await session.send_client_content(turns={"parts": [{"text": prompt}]})

            wf = wave.open("audio.wav", "wb")
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)  # Output is 24kHz

            async for response in session.receive():
                if response.data is not None:
                    wf.writeframes(response.data)
                elif response.tool_call:
                    print("The tool was called")
                    function_responses = []
                    for fc in response.tool_call.function_calls:
                        function_response = types.FunctionResponse(
                            id=fc.id,
                            name=fc.name,
                            response={ "result": "ok" } # simple, hard-coded function response
                        )
                        function_responses.append(function_response)

                    await session.send_tool_response(function_responses=function_responses)

            wf.close()

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    import { GoogleGenAI, Modality } from '@google/genai';
    import * as fs from "node:fs";
    import pkg from 'wavefile';  // npm install wavefile
    const { WaveFile } = pkg;

    const ai = new GoogleGenAI({});
    const model = 'gemini-3.1-flash-live-preview';

    // Simple function definitions
    const turn_on_the_lights = { name: "turn_on_the_lights" } // , description: '...', parameters: { ... }
    const turn_off_the_lights = { name: "turn_off_the_lights" }

    const tools = [{ functionDeclarations: [turn_on_the_lights, turn_off_the_lights] }]

    const config = {
      responseModalities: [Modality.AUDIO],
      tools: tools
    }

    async function live() {
      const responseQueue = [];

      async function waitMessage() {
        let done = false;
        let message = undefined;
        while (!done) {
          message = responseQueue.shift();
          if (message) {
            done = true;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 100));
          }
        }
        return message;
      }

      async function handleTurn() {
        const turns = [];
        let done = false;
        while (!done) {
          const message = await waitMessage();
          turns.push(message);
          if (message.serverContent && message.serverContent.turnComplete) {
            done = true;
          } else if (message.toolCall) {
            done = true;
          }
        }
        return turns;
      }

      const session = await ai.live.connect({
        model: model,
        callbacks: {
          onopen: function () {
            console.debug('Opened');
          },
          onmessage: function (message) {
            responseQueue.push(message);
          },
          onerror: function (e) {
            console.debug('Error:', e.message);
          },
          onclose: function (e) {
            console.debug('Close:', e.reason);
          },
        },
        config: config,
      });

      const inputTurns = 'Turn on the lights please';
      session.sendClientContent({ turns: inputTurns });

      let turns = await handleTurn();

      for (const turn of turns) {
        if (turn.toolCall) {
          console.debug('A tool was called');
          const functionResponses = [];
          for (const fc of turn.toolCall.functionCalls) {
            functionResponses.push({
              id: fc.id,
              name: fc.name,
              response: { result: "ok" } // simple, hard-coded function response
            });
          }

          console.debug('Sending tool response...\n');
          session.sendToolResponse({ functionResponses: functionResponses });
        }
      }

      // Check again for new messages
      turns = await handleTurn();

      // Combine audio data strings and save as wave file
      const combinedAudio = turns.reduce((acc, turn) => {
          if (turn.data) {
              const buffer = Buffer.from(turn.data, 'base64');
              const intArray = new Int16Array(buffer.buffer, buffer.byteOffset, buffer.byteLength / Int16Array.BYTES_PER_ELEMENT);
              return acc.concat(Array.from(intArray));
          }
          return acc;
      }, []);

      const audioBuffer = new Int16Array(combinedAudio);

      const wf = new WaveFile();
      wf.fromScratch(1, 24000, '16', audioBuffer);  // output is 24kHz
      fs.writeFileSync('audio.wav', wf.toBuffer());

      session.close();
    }

    async function main() {
      await live().catch((e) => console.error('got error', e));
    }

    main();

From a single prompt, the model can generate multiple function calls and the
code necessary to chain their outputs. This code executes in a sandbox
environment, generating subsequent [BidiGenerateContentToolCall](https://ai.google.dev/api/live#bidigeneratecontenttoolcall) messages.

## Asynchronous function calling

Function calling executes sequentially by default, meaning execution pauses
until the results of each function call are available. This ensures sequential
processing, which means you won't be able to continue interacting with the model
while the functions are being run.

> [!NOTE]
> **Note:** Asynchronous function calling is not yet supported in Gemini 3.1 Flash Live. The model will not start responding until you've sent the tool response.

If you don't want to block the conversation, you can tell the model to run the
functions asynchronously. To do so, you first need to add a `behavior` to the
function definitions:

### Python

    # Non-blocking function definitions
    turn_on_the_lights = {"name": "turn_on_the_lights", "behavior": "NON_BLOCKING"} # turn_on_the_lights will run asynchronously
    turn_off_the_lights = {"name": "turn_off_the_lights"} # turn_off_the_lights will still pause all interactions with the model

### JavaScript

    import { GoogleGenAI, Modality, Behavior } from '@google/genai';

    // Non-blocking function definitions
    const turn_on_the_lights = {name: "turn_on_the_lights", behavior: Behavior.NON_BLOCKING}

    // Blocking function definitions
    const turn_off_the_lights = {name: "turn_off_the_lights"}

    const tools = [{ functionDeclarations: [turn_on_the_lights, turn_off_the_lights] }]

`NON-BLOCKING` ensures the function runs asynchronously while you can
continue interacting with the model.

Then you need to tell the model how to behave when it receives the
`FunctionResponse` using the `scheduling` parameter. It can either:

- Interrupt what it's doing and tell you about the response it got right away (`scheduling="INTERRUPT"`),
- Wait until it's finished with what it's currently doing (`scheduling="WHEN_IDLE"`),
- Or do nothing and use that knowledge later on in the discussion
  (`scheduling="SILENT"`)

### Python

    # for a non-blocking function definition, apply scheduling in the function response:
      function_response = types.FunctionResponse(
          id=fc.id,
          name=fc.name,
          response={
              "result": "ok",
              "scheduling": "INTERRUPT" # Can also be WHEN_IDLE or SILENT
          }
      )

### JavaScript

    import { GoogleGenAI, Modality, Behavior, FunctionResponseScheduling } from '@google/genai';

    // for a non-blocking function definition, apply scheduling in the function response:
    const functionResponse = {
      id: fc.id,
      name: fc.name,
      response: {
        result: "ok",
        scheduling: FunctionResponseScheduling.INTERRUPT  // Can also be WHEN_IDLE or SILENT
      }
    }

## Grounding with Google Search

You can enable Grounding with Google Search as part of the session
configuration. This increases the Live API's accuracy and prevents
hallucinations. See the [Grounding tutorial](https://ai.google.dev/gemini-api/docs/grounding) to
learn more.

### Python

    import asyncio
    import wave
    from google import genai
    from google.genai import types

    client = genai.Client()

    model = "gemini-3.1-flash-live-preview"

    tools = [{'google_search': {}}]
    config = {"response_modalities": ["AUDIO"], "tools": tools}

    async def main():
        async with client.aio.live.connect(model=model, config=config) as session:
            prompt = "When did the last Brazil vs. Argentina soccer match happen?"
            await session.send_client_content(turns={"parts": [{"text": prompt}]})

            wf = wave.open("audio.wav", "wb")
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)  # Output is 24kHz

            async for chunk in session.receive():
                if chunk.server_content:
                    if chunk.data is not None:
                        wf.writeframes(chunk.data)

                    # The model might generate and execute Python code to use Search
                    model_turn = chunk.server_content.model_turn
                    if model_turn:
                        for part in model_turn.parts:
                            if part.executable_code is not None:
                                print(part.executable_code.code)

                            if part.code_execution_result is not None:
                                print(part.code_execution_result.output)

            wf.close()

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    import { GoogleGenAI, Modality } from '@google/genai';
    import * as fs from "node:fs";
    import pkg from 'wavefile';  // npm install wavefile
    const { WaveFile } = pkg;

    const ai = new GoogleGenAI({});
    const model = 'gemini-3.1-flash-live-preview';

    const tools = [{ googleSearch: {} }]
    const config = {
      responseModalities: [Modality.AUDIO],
      tools: tools
    }

    async function live() {
      const responseQueue = [];

      async function waitMessage() {
        let done = false;
        let message = undefined;
        while (!done) {
          message = responseQueue.shift();
          if (message) {
            done = true;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 100));
          }
        }
        return message;
      }

      async function handleTurn() {
        const turns = [];
        let done = false;
        while (!done) {
          const message = await waitMessage();
          turns.push(message);
          if (message.serverContent && message.serverContent.turnComplete) {
            done = true;
          } else if (message.toolCall) {
            done = true;
          }
        }
        return turns;
      }

      const session = await ai.live.connect({
        model: model,
        callbacks: {
          onopen: function () {
            console.debug('Opened');
          },
          onmessage: function (message) {
            responseQueue.push(message);
          },
          onerror: function (e) {
            console.debug('Error:', e.message);
          },
          onclose: function (e) {
            console.debug('Close:', e.reason);
          },
        },
        config: config,
      });

      const inputTurns = 'When did the last Brazil vs. Argentina soccer match happen?';
      session.sendClientContent({ turns: inputTurns });

      let turns = await handleTurn();

      let combinedData = '';
      for (const turn of turns) {
        if (turn.serverContent && turn.serverContent.modelTurn && turn.serverContent.modelTurn.parts) {
          for (const part of turn.serverContent.modelTurn.parts) {
            if (part.executableCode) {
              console.debug('executableCode: %s\n', part.executableCode.code);
            }
            else if (part.codeExecutionResult) {
              console.debug('codeExecutionResult: %s\n', part.codeExecutionResult.output);
            }
            else if (part.inlineData && typeof part.inlineData.data === 'string') {
              combinedData += atob(part.inlineData.data);
            }
          }
        }
      }

      // Convert the base64-encoded string of bytes into a Buffer.
      const buffer = Buffer.from(combinedData, 'binary');

      // The buffer contains raw bytes. For 16-bit audio, we need to interpret every 2 bytes as a single sample.
      const intArray = new Int16Array(buffer.buffer, buffer.byteOffset, buffer.byteLength / Int16Array.BYTES_PER_ELEMENT);

      const wf = new WaveFile();
      // The API returns 16-bit PCM audio at a 24kHz sample rate.
      wf.fromScratch(1, 24000, '16', intArray);
      fs.writeFileSync('audio.wav', wf.toBuffer());

      session.close();
    }

    async function main() {
      await live().catch((e) => console.error('got error', e));
    }

    main();

## Combining multiple tools

You can combine multiple tools within the Live API,
increasing your application's capabilities even more:

### Python

    prompt = """
    Hey, I need you to do two things for me.

    1. Use Google Search to look up information about the largest earthquake in California the week of Dec 5 2024?
    2. Then turn on the lights

    Thanks!
    """

    tools = [
        {"google_search": {}},
        {"function_declarations": [turn_on_the_lights, turn_off_the_lights]},
    ]

    config = {"response_modalities": ["AUDIO"], "tools": tools}

    # ... remaining model call

### JavaScript

    const prompt = `Hey, I need you to do two things for me.

    1. Use Google Search to look up information about the largest earthquake in California the week of Dec 5 2024?
    2. Then turn on the lights

    Thanks!
    `

    const tools = [
      { googleSearch: {} },
      { functionDeclarations: [turn_on_the_lights, turn_off_the_lights] }
    ]

    const config = {
      responseModalities: [Modality.AUDIO],
      tools: tools
    }

    // ... remaining model call

## What's next

- Check out more examples of using tools with the Live API in the [Tool use cookbook](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_LiveAPI_tools.ipynb).
- Get the full story on features and configurations from the [Live API Capabilities guide](https://ai.google.dev/gemini-api/docs/live-guide).



In the Live API, a session refers to a persistent
connection where input and output are streamed continuously over the same
connection (read more about [how it works](https://ai.google.dev/gemini-api/docs/live)).
This unique session design enables low latency and supports unique features, but
can also introduce challenges, like session time limits, and early termination.
This guide covers strategies for overcoming the session management challenges
that can arise when using the Live API.

## Session lifetime

Without compression, audio-only sessions are limited to 15 minutes,
and audio-video sessions are limited to 2 minutes. Exceeding these limits
will terminate the session (and therefore, the connection), but you can use
[context window compression](https://ai.google.dev/gemini-api/docs/live-api/session-management#context-window-compression) to extend sessions to
an unlimited amount of time.

The lifetime of a connection is limited as well, to around 10 minutes. When the
connection terminates, the session terminates as well. In this case, you can
configure a single session to stay active over multiple connections using
[session resumption](https://ai.google.dev/gemini-api/docs/live-api/session-management#session-resumption).
You'll also receive a [GoAway message](https://ai.google.dev/gemini-api/docs/live-api/session-management#goaway-message) before the
connection ends, allowing you to take further actions.

## Context window compression

To enable longer sessions, and avoid abrupt connection termination, you can
enable context window compression by setting the [contextWindowCompression](https://ai.google.dev/api/live#BidiGenerateContentSetup.FIELDS.ContextWindowCompressionConfig.BidiGenerateContentSetup.context_window_compression)
field as part of the session configuration.

In the [ContextWindowCompressionConfig](https://ai.google.dev/api/live#contextwindowcompressionconfig), you can configure a
[sliding-window mechanism](https://ai.google.dev/api/live#ContextWindowCompressionConfig.FIELDS.ContextWindowCompressionConfig.SlidingWindow.ContextWindowCompressionConfig.sliding_window)
and the [number of tokens](https://ai.google.dev/api/live#ContextWindowCompressionConfig.FIELDS.int64.ContextWindowCompressionConfig.trigger_tokens)
that triggers compression.

### Python

    from google.genai import types

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        context_window_compression=(
            # Configures compression with default parameters.
            types.ContextWindowCompressionConfig(
                sliding_window=types.SlidingWindow(),
            )
        ),
    )

### JavaScript

    const config = {
      responseModalities: [Modality.AUDIO],
      contextWindowCompression: { slidingWindow: {} }
    };

## Session resumption

To prevent session termination when the server periodically resets the WebSocket
connection, configure the [sessionResumption](https://ai.google.dev/api/live#BidiGenerateContentSetup.FIELDS.SessionResumptionConfig.BidiGenerateContentSetup.session_resumption)
field within the [setup configuration](https://ai.google.dev/api/live#BidiGenerateContentSetup).

Passing this configuration causes the
server to send [SessionResumptionUpdate](https://ai.google.dev/api/live#SessionResumptionUpdate)
messages, which can be used to resume the session by passing the last resumption
token as the [`SessionResumptionConfig.handle`](https://ai.google.dev/api/live#SessionResumptionConfig.FIELDS.string.SessionResumptionConfig.handle)
of the subsequent connection.

Resumption tokens are valid for 2 hr after the last sessions termination.

### Python

    import asyncio
    from google import genai
    from google.genai import types

    client = genai.Client()
    model = "gemini-3.1-flash-live-preview"

    async def main():
        print(f"Connecting to the service with handle {previous_session_handle}...")
        async with client.aio.live.connect(
            model=model,
            config=types.LiveConnectConfig(
                response_modalities=["AUDIO"],
                session_resumption=types.SessionResumptionConfig(
                    # The handle of the session to resume is passed here,
                    # or else None to start a new session.
                    handle=previous_session_handle
                ),
            ),
        ) as session:
            while True:
                await session.send_client_content(
                    turns=types.Content(
                        role="user", parts=[types.Part(text="Hello world!")]
                    )
                )
                async for message in session.receive():
                    # Periodically, the server will send update messages that may
                    # contain a handle for the current state of the session.
                    if message.session_resumption_update:
                        update = message.session_resumption_update
                        if update.resumable and update.new_handle:
                            # The handle should be retained and linked to the session.
                            return update.new_handle

                    # For the purposes of this example, placeholder input is continually fed
                    # to the model. In non-sample code, the model inputs would come from
                    # the user.
                    if message.server_content and message.server_content.turn_complete:
                        break

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    import { GoogleGenAI, Modality } from '@google/genai';

    const ai = new GoogleGenAI({});
    const model = 'gemini-3.1-flash-live-preview';

    async function live() {
      const responseQueue = [];

      async function waitMessage() {
        let done = false;
        let message = undefined;
        while (!done) {
          message = responseQueue.shift();
          if (message) {
            done = true;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 100));
          }
        }
        return message;
      }

      async function handleTurn() {
        const turns = [];
        let done = false;
        while (!done) {
          const message = await waitMessage();
          turns.push(message);
          if (message.serverContent && message.serverContent.turnComplete) {
            done = true;
          }
        }
        return turns;
      }

    console.debug('Connecting to the service with handle %s...', previousSessionHandle)
    const session = await ai.live.connect({
      model: model,
      callbacks: {
        onopen: function () {
          console.debug('Opened');
        },
        onmessage: function (message) {
          responseQueue.push(message);
        },
        onerror: function (e) {
          console.debug('Error:', e.message);
        },
        onclose: function (e) {
          console.debug('Close:', e.reason);
        },
      },
      config: {
        responseModalities: [Modality.AUDIO],
        sessionResumption: { handle: previousSessionHandle }
        // The handle of the session to resume is passed here, or else null to start a new session.
      }
    });

    const inputTurns = 'Hello how are you?';
    session.sendClientContent({ turns: inputTurns });

    const turns = await handleTurn();
    for (const turn of turns) {
      if (turn.sessionResumptionUpdate) {
        if (turn.sessionResumptionUpdate.resumable && turn.sessionResumptionUpdate.newHandle) {
          let newHandle = turn.sessionResumptionUpdate.newHandle
          // ...Store newHandle and start new session with this handle here
        }
      }
    }

      session.close();
    }

    async function main() {
      await live().catch((e) => console.error('got error', e));
    }

    main();

## Receiving a message before the session disconnects

The server sends a [GoAway](https://ai.google.dev/api/live#GoAway) message that signals that the current
connection will soon be terminated. This message includes the [timeLeft](https://ai.google.dev/api/live#GoAway.FIELDS.google.protobuf.Duration.GoAway.time_left),
indicating the remaining time and lets you take further action before the
connection will be terminated as ABORTED.

### Python

    async for response in session.receive():
        if response.go_away is not None:
            # The connection will soon be terminated
            print(response.go_away.time_left)

### JavaScript

    const turns = await handleTurn();

    for (const turn of turns) {
      if (turn.goAway) {
        console.debug('Time left: %s\n', turn.goAway.timeLeft);
      }
    }

## Receiving a message when the generation is complete

The server sends a [generationComplete](https://ai.google.dev/api/live#BidiGenerateContentServerContent.FIELDS.bool.BidiGenerateContentServerContent.generation_complete)
message that signals that the model finished generating the response.

### Python

    async for response in session.receive():
        if response.server_content.generation_complete is True:
            # The generation is complete

### JavaScript

    const turns = await handleTurn();

    for (const turn of turns) {
      if (turn.serverContent && turn.serverContent.generationComplete) {
        // The generation is complete
      }
    }

## What's next

Explore more ways to work with the Live API in the full
[Capabilities](https://ai.google.dev/gemini-api/docs/live) guide,
the [Tool use](https://ai.google.dev/gemini-api/docs/live-tools) page, or the
[Live API cookbook](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_LiveAPI.ipynb).



In the Live API, a session refers to a persistent
connection where input and output are streamed continuously over the same
connection (read more about [how it works](https://ai.google.dev/gemini-api/docs/live)).
This unique session design enables low latency and supports unique features, but
can also introduce challenges, like session time limits, and early termination.
This guide covers strategies for overcoming the session management challenges
that can arise when using the Live API.

## Session lifetime

Without compression, audio-only sessions are limited to 15 minutes,
and audio-video sessions are limited to 2 minutes. Exceeding these limits
will terminate the session (and therefore, the connection), but you can use
[context window compression](https://ai.google.dev/gemini-api/docs/live-api/session-management#context-window-compression) to extend sessions to
an unlimited amount of time.

The lifetime of a connection is limited as well, to around 10 minutes. When the
connection terminates, the session terminates as well. In this case, you can
configure a single session to stay active over multiple connections using
[session resumption](https://ai.google.dev/gemini-api/docs/live-api/session-management#session-resumption).
You'll also receive a [GoAway message](https://ai.google.dev/gemini-api/docs/live-api/session-management#goaway-message) before the
connection ends, allowing you to take further actions.

## Context window compression

To enable longer sessions, and avoid abrupt connection termination, you can
enable context window compression by setting the [contextWindowCompression](https://ai.google.dev/api/live#BidiGenerateContentSetup.FIELDS.ContextWindowCompressionConfig.BidiGenerateContentSetup.context_window_compression)
field as part of the session configuration.

In the [ContextWindowCompressionConfig](https://ai.google.dev/api/live#contextwindowcompressionconfig), you can configure a
[sliding-window mechanism](https://ai.google.dev/api/live#ContextWindowCompressionConfig.FIELDS.ContextWindowCompressionConfig.SlidingWindow.ContextWindowCompressionConfig.sliding_window)
and the [number of tokens](https://ai.google.dev/api/live#ContextWindowCompressionConfig.FIELDS.int64.ContextWindowCompressionConfig.trigger_tokens)
that triggers compression.

### Python

    from google.genai import types

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        context_window_compression=(
            # Configures compression with default parameters.
            types.ContextWindowCompressionConfig(
                sliding_window=types.SlidingWindow(),
            )
        ),
    )

### JavaScript

    const config = {
      responseModalities: [Modality.AUDIO],
      contextWindowCompression: { slidingWindow: {} }
    };

## Session resumption

To prevent session termination when the server periodically resets the WebSocket
connection, configure the [sessionResumption](https://ai.google.dev/api/live#BidiGenerateContentSetup.FIELDS.SessionResumptionConfig.BidiGenerateContentSetup.session_resumption)
field within the [setup configuration](https://ai.google.dev/api/live#BidiGenerateContentSetup).

Passing this configuration causes the
server to send [SessionResumptionUpdate](https://ai.google.dev/api/live#SessionResumptionUpdate)
messages, which can be used to resume the session by passing the last resumption
token as the [`SessionResumptionConfig.handle`](https://ai.google.dev/api/live#SessionResumptionConfig.FIELDS.string.SessionResumptionConfig.handle)
of the subsequent connection.

Resumption tokens are valid for 2 hr after the last sessions termination.

### Python

    import asyncio
    from google import genai
    from google.genai import types

    client = genai.Client()
    model = "gemini-3.1-flash-live-preview"

    async def main():
        print(f"Connecting to the service with handle {previous_session_handle}...")
        async with client.aio.live.connect(
            model=model,
            config=types.LiveConnectConfig(
                response_modalities=["AUDIO"],
                session_resumption=types.SessionResumptionConfig(
                    # The handle of the session to resume is passed here,
                    # or else None to start a new session.
                    handle=previous_session_handle
                ),
            ),
        ) as session:
            while True:
                await session.send_client_content(
                    turns=types.Content(
                        role="user", parts=[types.Part(text="Hello world!")]
                    )
                )
                async for message in session.receive():
                    # Periodically, the server will send update messages that may
                    # contain a handle for the current state of the session.
                    if message.session_resumption_update:
                        update = message.session_resumption_update
                        if update.resumable and update.new_handle:
                            # The handle should be retained and linked to the session.
                            return update.new_handle

                    # For the purposes of this example, placeholder input is continually fed
                    # to the model. In non-sample code, the model inputs would come from
                    # the user.
                    if message.server_content and message.server_content.turn_complete:
                        break

    if __name__ == "__main__":
        asyncio.run(main())

### JavaScript

    import { GoogleGenAI, Modality } from '@google/genai';

    const ai = new GoogleGenAI({});
    const model = 'gemini-3.1-flash-live-preview';

    async function live() {
      const responseQueue = [];

      async function waitMessage() {
        let done = false;
        let message = undefined;
        while (!done) {
          message = responseQueue.shift();
          if (message) {
            done = true;
          } else {
            await new Promise((resolve) => setTimeout(resolve, 100));
          }
        }
        return message;
      }

      async function handleTurn() {
        const turns = [];
        let done = false;
        while (!done) {
          const message = await waitMessage();
          turns.push(message);
          if (message.serverContent && message.serverContent.turnComplete) {
            done = true;
          }
        }
        return turns;
      }

    console.debug('Connecting to the service with handle %s...', previousSessionHandle)
    const session = await ai.live.connect({
      model: model,
      callbacks: {
        onopen: function () {
          console.debug('Opened');
        },
        onmessage: function (message) {
          responseQueue.push(message);
        },
        onerror: function (e) {
          console.debug('Error:', e.message);
        },
        onclose: function (e) {
          console.debug('Close:', e.reason);
        },
      },
      config: {
        responseModalities: [Modality.AUDIO],
        sessionResumption: { handle: previousSessionHandle }
        // The handle of the session to resume is passed here, or else null to start a new session.
      }
    });

    const inputTurns = 'Hello how are you?';
    session.sendClientContent({ turns: inputTurns });

    const turns = await handleTurn();
    for (const turn of turns) {
      if (turn.sessionResumptionUpdate) {
        if (turn.sessionResumptionUpdate.resumable && turn.sessionResumptionUpdate.newHandle) {
          let newHandle = turn.sessionResumptionUpdate.newHandle
          // ...Store newHandle and start new session with this handle here
        }
      }
    }

      session.close();
    }

    async function main() {
      await live().catch((e) => console.error('got error', e));
    }

    main();

## Receiving a message before the session disconnects

The server sends a [GoAway](https://ai.google.dev/api/live#GoAway) message that signals that the current
connection will soon be terminated. This message includes the [timeLeft](https://ai.google.dev/api/live#GoAway.FIELDS.google.protobuf.Duration.GoAway.time_left),
indicating the remaining time and lets you take further action before the
connection will be terminated as ABORTED.

### Python

    async for response in session.receive():
        if response.go_away is not None:
            # The connection will soon be terminated
            print(response.go_away.time_left)

### JavaScript

    const turns = await handleTurn();

    for (const turn of turns) {
      if (turn.goAway) {
        console.debug('Time left: %s\n', turn.goAway.timeLeft);
      }
    }

## Receiving a message when the generation is complete

The server sends a [generationComplete](https://ai.google.dev/api/live#BidiGenerateContentServerContent.FIELDS.bool.BidiGenerateContentServerContent.generation_complete)
message that signals that the model finished generating the response.

### Python

    async for response in session.receive():
        if response.server_content.generation_complete is True:
            # The generation is complete

### JavaScript

    const turns = await handleTurn();

    for (const turn of turns) {
      if (turn.serverContent && turn.serverContent.generationComplete) {
        // The generation is complete
      }
    }

## What's next

Explore more ways to work with the Live API in the full
[Capabilities](https://ai.google.dev/gemini-api/docs/live) guide,
the [Tool use](https://ai.google.dev/gemini-api/docs/live-tools) page, or the
[Live API cookbook](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_LiveAPI.ipynb).



> [!WARNING]
> **Preview:** The Live API is in preview.

This guide covers best practices you can follow to
optimize your use of the Live API.
See [Get started with Live API](https://ai.google.dev/gemini-api/docs/live)
page for an overview and sample code for common use cases.

## Design clear system instructions

To get the best performance out of Live API, we recommend having a
clearly-defined set of system instructions (SIs) that defines the agent persona,
conversational rules, and guardrails, in this order.

For best results, separate each agent into a distinct SI.

1. **Specify the agent persona:** Provide detail on the agent's name, role, and
   any preferred characteristics. If you want to specify the accent, be sure to
   also specify the preferred output language (such as a British accent for an
   English speaker).

2. **Specify the conversational rules:** Put these rules in the order you expect
   the model to follow. Delineate between one-time elements of the conversation
   and conversational loops. For example:

   - **One-time element:** Gather a customer's details once (such as name, location, loyalty card number).
   - **Conversational loop:** The user can discuss recommendations, pricing, returns, and delivery, and may want to go from topic to topic. Let the model know that it's OK to engage in this conversational loop for as long as the user wants.
3. **Specify tool calls within a flow in distinct sentences:** For example, if a
   one-time step to gather a customer's details requires invoking a `get_user_info`
   function, you might say: *Your first step is to gather user information. First,
   ask the user to provide their name, location, and loyalty card number. Then
   invoke `get_user_info` with these details.*

4. **Add any necessary guardrails:** Provide any general conversational
   guardrails you don't want the model to do. Feel free to provide specific
   examples of if *x* happens, you want the model to do *y* . If you're still not
   getting the preferred level of precision, use the word
   *unmistakably* to guide the model to be precise.

## Define tools precisely

When using tools with Live API, be specific in your tool definitions.
Be sure to tell Gemini under what conditions a tool call should be
invoked. For more details, see [Tool definitions](https://ai.google.dev/gemini-api/docs/live-api/best-practices#tool-definitions-example) in
the example section.

## Craft effective prompts

- **Use clear prompts:** Provide examples of what the models should and shouldn't do in the prompts, and try to limit prompts to one prompt per persona or role at a time. Instead of lengthy, multi-page prompts, consider using prompt chaining instead. The model performs best on tasks with single function calls.
- **Provide starting commands and information:** Live API expects user input before it responds. To have Live API initiate the conversation, include a prompt asking it to greet the user or begin the conversation. Include information about the user to have Live API personalize that greeting.

## Specify language

For optimal performance on Live API cascaded `gemini-live-2.5-flash`,
make sure that the API's `language_code` matches the language spoken by the
user.

If the expectation is for the model to respond in a non-English language,
include the following as part of your system instructions:

    RESPOND IN {OUTPUT_LANGUAGE}. YOU MUST RESPOND UNMISTAKABLY IN {OUTPUT_LANGUAGE}.

## Streaming

When implementing real-time audio, follow these best practices:

- **Chunk Size and Latency**: Send audio in chunks of 20ms to 40ms.
- **Interruption Handling** : When the user speaks while the model is replying, the server sends a `server_content` message with `"interrupted": true`. You must immediately discard your client-side audio buffer to prevent the agent from continuing to talk over the user.

## Context management

Use `ContextWindowCompressionConfig` for long sessions, as native audio tokens
accumulate rapidly (approximately 25 tokens per sec of audio).

## Client buffering

Don't buffer input audio significantly (such as 1 second) before sending. Send
small chunks (20ms - 100ms) to minimize latency.

## Resampling

Ensure your client application resamples microphone input (often 44.1kHz or
48kHz) to 16kHz before transmission.

## Session management

Follow these guidelines to handle session lifecycle and ensure a reliable user
experience:

- **Enable context window compression:** Audio tokens accumulate at approximately 25 tokens per second. Without compression, audio-only sessions are limited to 15 minutes and audio-video sessions to 2 minutes. Enable [context window compression](https://ai.google.dev/gemini-api/docs/live-api/session-management#context-window-compression) to extend sessions to an unlimited duration.
- **Implement session resumption:** The server may periodically reset the WebSocket connection. Use [session resumption](https://ai.google.dev/gemini-api/docs/live-api/session-management#session-resumption) to seamlessly reconnect without losing context. Retain the latest resumption token from `SessionResumptionUpdate` messages and pass it as the handle when reconnecting. Resumption tokens are valid for 2 hours after the last session terminates.
- **Handle GoAway messages:** The server sends a [GoAway](https://ai.google.dev/gemini-api/docs/live-api/session-management#goaway-message) message before terminating a connection. Listen for this message and use the `timeLeft` field to gracefully wrap up or reconnect before the connection closes.
- **Handle generationComplete signals:** Use the [`generationComplete`](https://ai.google.dev/gemini-api/docs/live-api/session-management#generation-complete-message) message to know when the model has finished generating a response, so your application can update its UI or proceed with the next action.

For implementation details, see
[Session management](https://ai.google.dev/gemini-api/docs/live-api/session-management).

## Examples

This example combines both the best practices and
[guidelines for system instruction design](https://ai.google.dev/gemini-api/docs/live-api/best-practices#system-instruction-guidelines) to
guide the model's performance as a career coach.

    **Persona:**
    You are Laura, a career coach from Brooklyn, NY. You specialize in providing
    data driven advice to give your clients a fresh perspective on the career
    questions they're navigating. Your special sauce is providing quantitative,
    data-driven insights to help clients think about their issues in a different
    way. You leverage statistics, research, and psychology as much as possible.
    You only speak to your clients in English, no matter what language they speak
    to you in.

    **Conversational Rules:**

    1. **Introduce yourself:** Warmly greet the client.

    2. **Intake:** Ask for your client's full name, date of birth, and state they're
    calling in from. Call `create_client_profile` to create a new patient profile.

    3. **Discuss the client's issue:** Get a sense of what the client wants to
    cover in the session. DO NOT repeat what the client is saying back to them in
    your response. Don't ask more than a few questions here.

    4. **Reframe the client's issue with real data:** NO PLATITUDES. Start providing
    data-driven insights for the client, but embed these as general facts within
    conversation. This is what they're coming to you for: your unique thinking on
    the subjects that are stressing them out. Show them a new way of thinking about
    something. Let this step go on for as long as the client wants. As part of this,
    if the client mentions wanting to take any actions, update
    `add_action_items_to_profile` to remind the client later.

    5. **Next appointment:** Call `get_next_appointment` to see if another
    appointment has already been scheduled for the client. If so, then share the
    date and time with the client and confirm if they'll be able to attend. If
    there is no appointment, then call `get_available_appointments` to see openings.
    Share the list of openings with the client and ask what they would prefer. Save
    their preference with `schedule_appointment`. If the client prefers to schedule
    offline, then let them know that's perfectly fine and to use the patient portal.

    **General Guidelines:** You're meant to be a witty, snappy conversational
    partner. Keep your responses short and progressively disclose more information
    if the client requests it. Don't repeat back what the client says back to them.
    Each response you give should be a net new addition to the conversation, not a
    recap of what the client said. Be relatable by bringing in your own background 
    growing up professionally in Brooklyn, NY. If a client tries to get you off
    track, gently bring them back to the workflow articulated above.

    **Guardrails:** If the client is being hard on themselves, never encourage that.
    Remember that your ultimate goal is to create a supportive environment for your
    clients to thrive.

### Tool definitions

This JSON defines the relevant functions called in the career coach example.
For best results when defining functions, include their names, descriptions,
parameters, and invocation conditions.

    [
     {
       "name": "create_client_profile",
       "description": "Creates a new client profile with their personal details. Returns a unique client ID. \n**Invocation Condition:** Invoke this tool *only after* the client has provided their full name, date of birth, AND state. This should only be called once at the beginning of the 'Intake' step.",
       "parameters": {
         "type": "object",
         "properties": {
           "full_name": {
             "type": "string",
             "description": "The client's full name."
           },
           "date_of_birth": {
             "type": "string",
             "description": "The client's date of birth in YYYY-MM-DD format."
           },
           "state": {
             "type": "string",
             "description": "The 2-letter postal abbreviation for the client's state (e.g., 'NY', 'CA')."
           }
         },
         "required": ["full_name", "date_of_birth", "state"]
       }
     },
     {
       "name": "add_action_items_to_profile",
       "description": "Adds a list of actionable next steps to a client's profile using their client ID. \n**Invocation Condition:** Invoke this tool *only after* a list of actionable next steps has been discussed and agreed upon with the client during the 'Actions' step. Requires the `client_id` obtained from the start of the session.",
       "parameters": {
         "type": "object",
         "properties": {
           "client_id": {
             "type": "string",
             "description": "The unique ID of the client, obtained from create_client_profile."
           },
           "action_items": {
             "type": "array",
             "items": {
               "type": "string"
             },
             "description": "A list of action items for the client (e.g., ['Update resume', 'Research three companies'])."
           }
         },
         "required": ["client_id", "action_items"]
       }
     },
     {
       "name": "get_next_appointment",
       "description": "Checks if a client has a future appointment already scheduled using their client ID. Returns the appointment details or null. \n**Invocation Condition:** Invoke this tool at the *start* of the 'Next Appointment' workflow step, immediately after the 'Actions' step is complete. This is used to check if an appointment *already exists*.",
       "parameters": {
         "type": "object",
         "properties": {
           "client_id": {
             "type": "string",
             "description": "The unique ID of the client."
           }
         },
         "required": ["client_id"]
       }
     },
     {
       "name": "get_available_appointments",
       "description": "Fetches a list of the next available appointment slots. \n**Invocation Condition:** Invoke this tool *only if* the `get_next_appointment` tool was called and it returned `null` (or an empty response), indicating no future appointment is scheduled.",
       "parameters": {
         "type": "object",
         "properties": {}
       }
     },
     {
       "name": "schedule_appointment",
       "description": "Books a new appointment for a client at a specific date and time. \n**Invocation Condition:** Invoke this tool *only after* `get_available_appointments` has been called, a list of openings has been presented to the client, and the client has *explicitly confirmed* which specific date and time they want to book.",
       "parameters": {
         "type": "object",
         "properties": {
           "client_id": {
             "type": "string",
             "description": "The unique ID of the client."
           },
           "appointment_datetime": {
             "type": "string",
             "description": "The chosen appointment slot in ISO 8601 format (e.g., '2025-10-30T14:30:00')."
           }
         },
         "required": ["client_id", "appointment_datetime"]
       }
     }
    ]

## Pricing and billing

The Gemini Live API bills strictly by token usage. Because the Live API maintains a persistent WebSocket session, billing follows a compounding model based on the active context window.

### The session context window (compounding costs)

The API charges you per turn for all tokens present in the session context window. A "turn" is defined as one user input and the model's corresponding response.

- **Accumulation:** The context window includes new tokens from the current turn plus all accumulated tokens from previous turns.
- **Re-billing:** Past tokens are re-processed and accounted for in each new turn, up to your configured context window size. As a session lengthens, the cost per turn increases because the conversational history is re-processed.

### Audio tokens and transcriptions

The Live API is natively multimodal. It retains conversational history as raw audio tokens to preserve acoustic nuance and tone.

- **Audio billing:** The API bills you for the accumulated native audio tokens at the standard audio input rate on every turn.
- **Transcription surcharge:** When audio-to-text transcription is enabled (`inputAudioTranscription` or `outputAudioTranscription`), the API charges for all text tokens generated for transcription at the text token output rate in addition to the standard audio token costs.

### Managing costs with context limits

To prevent unbounded cost growth in long sessions, configure your context window size using `contextWindowCompression`.

By setting a compression trigger (e.g., 25,000 tokens) and a sliding window (e.g., 8,000 tokens), the API automatically evicts older tokens once the threshold is reached. The API then bills subsequent turns only for the retained history plus any new tokens.

### Proactive audio mode

When Proactive Audio Mode is enabled, input tokens are charged the entire time the Live API is listening, while output tokens are only charged when the API responds.

- **Note for Gemini 3.1:** Proactive Audio Mode is not supported in `gemini-3.1-flash-live-preview`. For this model, you are only billed for audio when actively streaming input.

For detailed pricing information, see the [Gemini API pricing page](https://ai.google.dev/gemini-api/docs/pricing).




