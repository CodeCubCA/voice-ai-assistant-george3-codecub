# Voice AI Assistant

> 🎯 **Portfolio Project by CodeCub CA**

An intelligent AI chatbot with voice input and output capabilities, powered by Google Gemini AI. Features multiple AI personalities, voice-to-text input, and text-to-speech output for a complete conversational experience.

## 🖼️ Project Showcase

![Voice AI Assistant Interface](screenshot.png)

### ✨ Design Highlights

- **🎨 Modern UI/UX**: Beautiful animated gradient background with smooth color transitions
- **💎 Glassmorphism Effects**: Sleek, semi-transparent design elements with backdrop blur
- **🎭 Interactive Elements**: Hover effects, animations, and responsive components
- **🌈 Premium Styling**: Custom CSS with professional typography using Google's Inter font
- **📱 Responsive Layout**: Clean, wide layout optimized for desktop and tablet use

### 🎯 Key Features Demonstrated

This project showcases my skills in:
- **Frontend Development**: Advanced CSS animations, glassmorphism, and modern UI patterns
- **API Integration**: Google Gemini AI, Speech Recognition, and Text-to-Speech APIs
- **Python Development**: Clean, modular code structure with session state management
- **UX Design**: Intuitive voice and text input methods with visual feedback

## Features

- 🎤 **Voice Input** - Speak directly to the AI using your microphone with Web Speech API
- 🔊 **Voice Output** - AI responses are automatically converted to speech using Google Text-to-Speech
- 💬 **Text Input** - Type your messages for traditional chat interaction
- 🗣️ **Voice-Only Mode** - Toggle to have AI respond with voice only (no text display)
- 🎯 **Auto-Play Voice** - Option to automatically play AI voice responses
- 🤖 **Multiple AI Personalities**:
  - General Assistant - Helpful and friendly for everyday tasks
  - Study Buddy - Patient learning companion for education
  - Fitness Coach - Motivating health and fitness guidance
  - Gaming Helper - Knowledgeable gaming companion
- 💾 **Chat History** - Maintains conversation context throughout your session
- 🎨 **Polished UI** - User-friendly interface with clear instructions and controls
- ⚡ **Streaming Responses** - Real-time AI response generation for faster interaction

## Technologies Used

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Google Gemini 2.5 Flash** - AI language model for intelligent conversations
- **SpeechRecognition** - Google Speech Recognition for voice-to-text conversion
- **gTTS (Google Text-to-Speech)** - Text-to-speech conversion for AI responses
- **audio-recorder-streamlit** - Browser-based audio recording component
- **python-dotenv** - Environment variable management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CodeCubCA/voice-ai-assistant-george3-codecub.git
cd voice-ai-assistant-george3-codecub
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Add your Google Gemini API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

4. Get your Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy it to your `.env` file

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser at `http://localhost:8501`

3. **Using Voice Input**:
   - Click the microphone button
   - Speak your message clearly
   - The AI will automatically transcribe and respond with both text and voice

4. **Using Text Input**:
   - Type your message in the text box at the bottom
   - Press Enter to send

5. **Voice Response Options**:
   - Enable "Auto-play AI voice responses" to hear responses automatically
   - Enable "Voice-only mode" for voice-only responses (no text display)

6. **Switching Personalities**:
   - Use the dropdown in the sidebar
   - Chat history clears when switching personalities

## Project Structure

```
voice-ai-assistant/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── .env.example       # Template for environment setup
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Requirements

- Python 3.8+
- Internet connection (for Google Speech Recognition and Gemini API)
- Microphone (for voice input)

## Dependencies

```
streamlit>=1.31.0
google-generativeai>=0.3.2
python-dotenv>=1.0.0
audio-recorder-streamlit>=0.0.8
SpeechRecognition>=3.10.0
gtts>=2.3.0
```

## Author

**CodeCub CA**
- GitHub: [@CodeCubCA](https://github.com/CodeCubCA)
- Repository: [voice-ai-assistant-george3-codecub](https://github.com/CodeCubCA/voice-ai-assistant-george3-codecub)

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Speech recognition by [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
