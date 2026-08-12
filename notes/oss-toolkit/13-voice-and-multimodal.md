# 13 Voice and Multimodal

> Voice agents are hard, which is exactly why a working one stands out in a portfolio.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| Whisper | Speech to text | The reference open speech recognition model covering 99 languages | Baseline transcription quality for any language | Python | MIT | Beginner | Very High | https://github.com/openai/whisper |
| faster-whisper | Speech to text | CTranslate2 reimplementation that is roughly four times faster with lower memory use | Production transcription on modest hardware | Python | MIT | Beginner | Very High | https://github.com/SYSTRAN/faster-whisper |
| whisper.cpp | Speech to text | Plain C and C++ port that runs on CPU, phones and browsers | On device transcription with no GPU | C++ | MIT | Intermediate | Very High | https://github.com/ggml-org/whisper.cpp |
| WhisperX | Speech to text | Adds word level timestamps and speaker diarisation on top of Whisper | Meeting transcripts that need who said what | Python | BSD-2 | Intermediate | High | https://github.com/m-bain/whisperX |
| NVIDIA NeMo | Speech toolkit | Full speech stack including ASR, TTS and speaker models with strong accuracy | Enterprise grade speech pipelines | Python | Apache-2.0 | Advanced | Very High | https://github.com/NVIDIA/NeMo |
| Silero VAD | Voice activity | Tiny fast model that detects when someone is actually speaking | Turn detection in a real time voice agent | Python | MIT | Beginner | Very High | https://github.com/snakers4/silero-vad |
| Kokoro | Text to speech | 82 million parameter TTS with quality far above its size, runs in real time on CPU | Cheap natural voice output at scale | Python | Apache-2.0 | Beginner | Very High | https://github.com/hexgrad/kokoro |
| Piper | Text to speech | Fast local neural TTS optimised for Raspberry Pi and low power devices | Offline voice on edge hardware | C++, Python | MIT | Beginner | High | https://github.com/rhasspy/piper |
| Coqui TTS | Text to speech | Long standing toolkit with XTTS voice cloning across many languages | Custom and cloned voices | Python | MPL-2.0 | Intermediate | Very High | https://github.com/coqui-ai/TTS |
| F5-TTS | Text to speech | Flow matching TTS with strong zero shot voice cloning from a short sample | High quality cloning without training | Python | MIT | Intermediate | High | https://github.com/SWivid/F5-TTS |
| ChatTTS | Text to speech | Conversational TTS tuned for natural dialogue with laughter and pauses | Agents that should sound like a person talking | Python | AGPL-3.0 | Intermediate | High | https://github.com/2noise/ChatTTS |
| Orpheus TTS | Text to speech | Llama based speech model with emotion tags and low latency streaming | Emotive real time agent voices | Python | Apache-2.0 | Intermediate | High | https://github.com/canopyai/Orpheus-TTS |
| Moshi | Speech to speech | Full duplex speech model that listens and speaks at the same time | Interruptible natural voice conversation | Python, Rust | Apache-2.0 and CC-BY | Advanced | High | https://github.com/kyutai-labs/moshi |
| Ultravox | Speech LLM | Multimodal model that consumes audio directly without a separate transcription step | Cutting a full hop of voice pipeline latency | Python | MIT | Advanced | High | https://github.com/fixie-ai/ultravox |
| Pipecat | Voice framework | Real time voice and multimodal agent framework with pluggable STT, LLM and TTS | Building a phone or web voice agent | Python | BSD-2 | Intermediate | Very High | https://github.com/pipecat-ai/pipecat |
| LiveKit Agents | Voice framework | Production voice agent framework on top of WebRTC with telephony support | Voice agents that must handle real phone calls | Python, Node | Apache-2.0 | Intermediate | Very High | https://github.com/livekit/agents |
| IndicTrans2 | Translation | Open translation models covering 22 scheduled Indian languages | Serving Indian users in their own language | Python | MIT | Intermediate | High | https://github.com/AI4Bharat/IndicTrans2 |
| ComfyUI | Image and video | Node based generation workflow engine that agents can drive through its API | Image and video generation as an agent tool | Python | GPL-3.0 | Intermediate | Very High | https://github.com/comfyanonymous/ComfyUI |
| SAM 2 | Vision | Meta promptable segmentation for images and video | Vision tools that need precise object masks | Python | Apache-2.0 | Advanced | Very High | https://github.com/facebookresearch/sam2 |
