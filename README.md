# Voice AI Assistant

A voice-enabled AI chatbot built with Streamlit and Google Gemini API, featuring multiple AI personalities and speech-to-text capabilities.

## Features

- 🎤 **Voice Input** - Speak directly to the AI using your microphone
- 💬 **Text Input** - Type your messages for traditional chat interaction
- 🤖 **Multiple AI Personalities**:
  - General Assistant - Helpful and friendly for everyday tasks
  - Study Buddy - Patient learning companion for education
  - Fitness Coach - Motivating health and fitness guidance
  - Gaming Helper - Knowledgeable gaming companion
- 💾 **Chat History** - Maintains conversation context throughout your session
- 🎨 **Clean UI** - User-friendly interface with clear instructions
- 🔄 **Auto-Response** - Voice messages automatically trigger AI responses

## Technologies Used

- **Streamlit** - Web application framework
- **Google Gemini 2.5 Flash** - AI language model
- **SpeechRecognition** - Google Speech Recognition for voice-to-text
- **audio-recorder-streamlit** - Browser-based audio recording
- **pydub** - Audio processing
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
   - The AI will automatically transcribe and respond

4. **Using Text Input**:
   - Type your message in the text box at the bottom
   - Press Enter to send

5. **Switching Personalities**:
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
pydub>=0.25.1
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
