import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import io
import tempfile
from gtts import gTTS
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Personality system prompts
PERSONALITIES = {
    "General Assistant": {
        "name": "General Assistant",
        "icon": "💬",
        "prompt": "You are a helpful and friendly AI assistant. Provide clear, accurate, and helpful responses to user questions."
    },
    "Study Buddy": {
        "name": "Study Buddy",
        "icon": "📚",
        "prompt": "You are a patient and encouraging study companion. Help users learn by explaining concepts clearly, breaking down complex topics, and providing examples. Use analogies when helpful and encourage critical thinking."
    },
    "Fitness Coach": {
        "name": "Fitness Coach",
        "icon": "💪",
        "prompt": "You are an enthusiastic and motivating fitness coach. Provide workout advice, nutrition tips, and encouragement. Focus on safe practices, proper form, and sustainable healthy habits. Always remind users to consult healthcare professionals for medical advice."
    },
    "Gaming Helper": {
        "name": "Gaming Helper",
        "icon": "🎮",
        "prompt": "You are a knowledgeable and enthusiastic gaming companion. Help with game strategies, tips, walkthroughs, and recommendations. Share gaming knowledge while maintaining a fun and casual tone."
    }
}

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None

if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}

if "processing" not in st.session_state:
    st.session_state.processing = False

if "auto_play_voice" not in st.session_state:
    st.session_state.auto_play_voice = False

if "voice_only_mode" not in st.session_state:
    st.session_state.voice_only_mode = False

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.markdown("---")

    # Personality selection
    st.subheader("Choose Personality")
    selected_personality = st.selectbox(
        "Select AI personality:",
        options=list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality)
    )

    # Update personality if changed
    if selected_personality != st.session_state.personality:
        st.session_state.personality = selected_personality
        st.session_state.messages = []  # Clear chat history when personality changes
        st.rerun()

    # Display personality info
    current_personality = PERSONALITIES[st.session_state.personality]
    st.info(f"{current_personality['icon']} **{current_personality['name']}**")

    st.markdown("---")
    st.subheader("About")
    st.write("This chatbot uses Google Gemini AI to provide intelligent responses based on the selected personality.")

    st.markdown("---")
    st.subheader("How to Use Voice Input")
    st.markdown("""
    1. Click the microphone button below
    2. Speak your message clearly
    3. The AI will automatically respond
    4. Or type your message if you prefer
    """)

    st.markdown("---")

    # Voice Response Toggle
    st.subheader("Voice Response")
    st.session_state.auto_play_voice = st.checkbox(
        "Auto-play AI voice responses",
        value=st.session_state.auto_play_voice,
        help="When enabled, AI responses will automatically play as audio"
    )

    st.session_state.voice_only_mode = st.checkbox(
        "Voice-only mode",
        value=st.session_state.voice_only_mode,
        help="When enabled, AI will respond with voice only (no text). When disabled, AI responds with text."
    )

    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.tts_audio = {}  # Clear cached audio too
        st.rerun()

# Function to process voice input
def transcribe_audio(audio_bytes):
    """Convert audio bytes to text using speech recognition."""
    temp_wav = None
    try:
        recognizer = sr.Recognizer()

        if not audio_bytes or len(audio_bytes) == 0:
            return None

        # Create temporary file and write audio bytes directly
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_wav = temp_file.name
        temp_file.write(audio_bytes)
        temp_file.close()

        # Verify file exists and has content
        if not os.path.exists(temp_wav) or os.path.getsize(temp_wav) == 0:
            st.error("Failed to create audio file")
            return None

        # Read with speech recognition
        with sr.AudioFile(temp_wav) as source:
            audio_data = recognizer.record(source)

        # Use Google Speech Recognition
        text = recognizer.recognize_google(audio_data, language="en-US")
        return text

    except sr.UnknownValueError:
        st.error("Could not understand audio. Please speak more clearly.")
        return None
    except sr.RequestError as e:
        st.error(f"Speech recognition error: {str(e)}. Please check your internet connection.")
        return None
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None
    finally:
        # Clean up temp file
        if temp_wav:
            try:
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
            except Exception:
                pass  # Ignore cleanup errors

# Function to generate TTS audio
def generate_tts_audio(text, message_index):
    """Generate text-to-speech audio for given text."""
    try:
        # Check if audio already exists for this message
        if message_index in st.session_state.tts_audio:
            return st.session_state.tts_audio[message_index]

        # Retry logic for rate limiting
        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                # Generate TTS audio
                tts = gTTS(text=text, lang='en', slow=False)

                # Save to BytesIO object
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)

                # Store in session state
                audio_data = audio_bytes.read()
                st.session_state.tts_audio[message_index] = audio_data

                return audio_data
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    # Rate limit error, wait and retry
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    raise e

    except Exception as e:
        if "429" in str(e):
            st.warning("TTS rate limit reached. Audio generation temporarily unavailable. Text response is still available.")
        else:
            st.error(f"TTS Error: {str(e)}")
        return None

# Function to generate AI response with streaming
def generate_ai_response_stream(prompt, placeholder):
    """Generate AI response with streaming for faster feedback."""
    try:
        # Create model with system instruction based on personality
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=PERSONALITIES[st.session_state.personality]["prompt"]
        )

        # Build conversation history for context
        chat_history = []
        for msg in st.session_state.messages[:-1]:  # Exclude the last message (current user input)
            chat_history.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            })

        # Start chat session with history
        chat = model.start_chat(history=chat_history)

        # Stream the response
        response = chat.send_message(prompt, stream=True)

        full_response = ""
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)
        return full_response

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        placeholder.markdown(error_msg)
        return error_msg

# Main chat interface
st.title(f"{PERSONALITIES[st.session_state.personality]['icon']} {st.session_state.personality}")
st.markdown("---")

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    # In voice-only mode, skip displaying text for assistant messages
    if not (st.session_state.voice_only_mode and message["role"] == "assistant"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display audio player for assistant messages (outside chat_message container)
    if message["role"] == "assistant":
        audio_data = generate_tts_audio(message["content"], i)
        if audio_data:
            # Auto-play for the most recent message if toggle is enabled OR if in voice-only mode
            autoplay = (st.session_state.auto_play_voice or st.session_state.voice_only_mode) and i == len(st.session_state.messages) - 1
            st.audio(audio_data, format='audio/mp3', autoplay=autoplay)

# Voice input section
st.markdown("### Voice Input")
col1, col2 = st.columns([1, 4])

with col1:
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="2x",
    )

with col2:
    if audio_bytes:
        # Check if this is a new recording by comparing bytes
        if st.session_state.last_audio_bytes is None or audio_bytes != st.session_state.last_audio_bytes:
            st.session_state.last_audio_bytes = audio_bytes

            with st.spinner("Transcribing audio..."):
                transcribed_text = transcribe_audio(audio_bytes)

            if transcribed_text:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": transcribed_text})

                # Generate AI response without displaying (will be shown after rerun)
                # Create a temporary placeholder for generation only
                with st.spinner("Generating response..."):
                    temp_placeholder = st.empty()
                    ai_response = generate_ai_response_stream(transcribed_text, temp_placeholder)
                    temp_placeholder.empty()  # Clear the temporary display

                # Add assistant message to history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

                # Clear the last audio bytes to allow new recordings
                st.session_state.last_audio_bytes = None
                st.rerun()
        else:
            st.info("Ready for your next message. Click the microphone to record.")

st.markdown("---")
st.markdown("### Text Input")

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response without displaying (will be shown after rerun)
    with st.spinner("Generating response..."):
        temp_placeholder = st.empty()
        ai_response = generate_ai_response_stream(prompt, temp_placeholder)
        temp_placeholder.empty()  # Clear the temporary display

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.rerun()
