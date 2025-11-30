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
        "prompt": "You are a helpful and friendly AI assistant. Speak naturally like a real person having a conversation. Keep responses conversational, warm, and engaging. Use casual language and contractions (like 'I'm', 'you're', 'let's'). Avoid overly formal or robotic language. Be concise but friendly, as if talking to a friend."
    },
    "Study Buddy": {
        "name": "Study Buddy",
        "icon": "📚",
        "prompt": "You are a patient and encouraging study companion who talks like a supportive friend. Speak naturally and conversationally. Use everyday language, contractions, and a warm tone. Explain concepts clearly with relatable examples. Say things like 'Hey, let me help you understand this' or 'That's a great question!' Keep it friendly and approachable, not formal or robotic."
    },
    "Fitness Coach": {
        "name": "Fitness Coach",
        "icon": "💪",
        "prompt": "You are an enthusiastic and motivating fitness coach who talks like an encouraging workout buddy. Speak naturally with energy and warmth. Use casual, motivating language like 'You've got this!' or 'Let's work on that together!' Keep it conversational and upbeat. Focus on safe practices and sustainable habits, but speak like a real person, not a formal trainer."
    },
    "Gaming Helper": {
        "name": "Gaming Helper",
        "icon": "🎮",
        "prompt": "You are a knowledgeable and enthusiastic gaming buddy. Talk like you're chatting with a friend about games - casual, fun, and natural. Use gaming slang when appropriate. Say things like 'Dude, here's what you should try' or 'That's awesome!' Keep it relaxed and conversational. Share tips and strategies like you're talking over voice chat with a friend."
    }
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None

if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}

if "voice_only_mode" not in st.session_state:
    st.session_state.voice_only_mode = False

if "response_length" not in st.session_state:
    st.session_state.response_length = "Medium"

# Page configuration
st.set_page_config(
    page_title="Voice AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Animated gradient background */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 2rem;
        min-height: 100vh;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar with DARK PURPLE/BLACK background and BRIGHT text */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d1b4e 0%, #1a0f2e 100%);
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(102, 126, 234, 0.5);
    }

    /* Make ALL sidebar text BRIGHT WHITE with text shadow for visibility */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.7);
        font-size: 1.3rem !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        font-size: 1.1rem !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Radio button styling for personality selection */
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.6);
    }

    [data-testid="stSidebar"] .stRadio {
        background: rgba(102, 126, 234, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }

    /* Enhanced chat messages with animation */
    .stChatMessage {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.95) 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: messageSlideIn 0.4s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stChatMessage:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
    }

    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Chat message text with better typography */
    .stChatMessage p {
        color: #1a202c !important;
        font-size: 1.05rem;
        line-height: 1.7;
        font-weight: 400;
    }

    .stChatMessage [data-testid="stMarkdownContainer"] {
        color: #1a202c !important;
    }

    /* Beautiful headers with glow effect */
    h1 {
        color: white;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.3), 2px 2px 4px rgba(0, 0, 0, 0.3);
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    h2 {
        color: white;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.2), 1px 1px 3px rgba(0, 0, 0, 0.2);
        font-weight: 700;
    }

    h3 {
        color: white;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.2), 1px 1px 2px rgba(0, 0, 0, 0.2);
        font-weight: 600;
    }

    /* Enhanced buttons with 3D effect */
    .stButton button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        border: none;
    }

    .stButton button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }

    .stButton button:active {
        transform: translateY(-1px) scale(0.98);
    }

    /* Modern input fields */
    .stTextInput input {
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.5);
        background: rgba(255, 255, 255, 0.95);
        transition: all 0.3s ease;
        padding: 0.75rem 1rem;
    }

    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background: white;
    }

    /* Smooth audio player */
    audio {
        width: 100%;
        border-radius: 12px;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
    }

    /* Animated spinner */
    .stSpinner > div {
        border-color: #667eea !important;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid rgba(102, 126, 234, 0.5);
        background: rgba(255, 255, 255, 0.95);
    }

    /* Checkbox styling */
    .stCheckbox {
        color: #e2e8f0;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #667eea; font-size: 2rem;'>🤖 Voice AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0aec0; margin-top: -10px;'>Your Intelligent Assistant</p>", unsafe_allow_html=True)
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

    # Response Length Selection
    st.subheader("⚡ Response Length")

    # Custom styled buttons with HTML
    st.markdown("""
    <style>
    .response-btn-container {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    .response-btn {
        flex: 1;
        padding: 0.75rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .response-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .response-btn-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .response-btn-inactive {
        background: rgba(255, 255, 255, 0.1);
        color: #a0aec0;
        border-color: rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Short", use_container_width=True, type="primary" if st.session_state.response_length == "Short" else "secondary"):
            st.session_state.response_length = "Short"
            st.rerun()

    with col2:
        if st.button("💬 Medium", use_container_width=True, type="primary" if st.session_state.response_length == "Medium" else "secondary"):
            st.session_state.response_length = "Medium"
            st.rerun()

    with col3:
        if st.button("📖 Long", use_container_width=True, type="primary" if st.session_state.response_length == "Long" else "secondary"):
            st.session_state.response_length = "Long"
            st.rerun()

    # Display current selection with an icon
    st.markdown(f"""
    <div style='text-align: center; margin-top: 0.5rem; padding: 0.5rem; background: rgba(102, 126, 234, 0.2); border-radius: 8px;'>
        <span style='color: #667eea; font-weight: 600;'>✨ {st.session_state.response_length}</span>
        <span style='color: #a0aec0;'> responses</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Voice-only mode toggle
    st.subheader("Voice Settings")
    st.session_state.voice_only_mode = st.checkbox(
        "Voice-only mode",
        value=st.session_state.voice_only_mode,
        help="When enabled, AI will respond with voice only (no text). When disabled, AI responds with text and voice."
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

        # Adjust for ambient noise
        recognizer.energy_threshold = 4000
        recognizer.dynamic_energy_threshold = True

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
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

        # Use Google Speech Recognition with language options
        text = recognizer.recognize_google(
            audio_data,
            language="en-US",
            show_all=False
        )
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
                # Generate TTS audio with natural voice settings
                # Use a more conversational speaking style
                tts = gTTS(text=text, lang='en', slow=False, tld='com')

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
def generate_ai_response_stream(prompt):
    """Generate AI response with streaming for faster feedback."""
    try:
        # Build system instruction with response length guidance
        length_instructions = {
            "Short": "IMPORTANT: Keep responses VERY brief - aim for 1-3 sentences maximum. Be direct and concise.",
            "Medium": "Keep responses moderate - around 3-5 sentences. Balance brevity with completeness.",
            "Long": "Provide detailed, comprehensive responses - 6+ sentences. Include explanations, examples, and context."
        }

        base_prompt = PERSONALITIES[st.session_state.personality]["prompt"]
        full_prompt = f"{base_prompt}\n\nResponse Length Guideline: {length_instructions[st.session_state.response_length]}"

        # Create model with system instruction based on personality
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=full_prompt
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

        return full_response

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return error_msg

# Main chat interface with beautiful animated header
st.markdown(f"""
<style>
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}

    @keyframes glow {{
        0%, 100% {{ box-shadow: 0 0 20px rgba(255, 255, 255, 0.2), 0 0 40px rgba(102, 126, 234, 0.3); }}
        50% {{ box-shadow: 0 0 30px rgba(255, 255, 255, 0.4), 0 0 60px rgba(102, 126, 234, 0.5); }}
    }}

    .hero-header {{
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
        border-radius: 25px;
        margin-bottom: 2.5rem;
        animation: glow 3s ease-in-out infinite;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }}

    .hero-icon {{
        font-size: 4rem;
        margin: 0;
        animation: pulse 2s ease-in-out infinite;
        display: inline-block;
    }}
</style>

<div class='hero-header'>
    <div class='hero-icon'>{PERSONALITIES[st.session_state.personality]['icon']}</div>
    <h2 style='color: white; margin: 1rem 0 0.5rem 0; font-weight: 700; font-size: 2.2rem;'>{st.session_state.personality}</h2>
    <p style='color: rgba(255, 255, 255, 0.9); margin: 0; font-size: 1.15rem; font-weight: 500;'>✨ Powered by Google Gemini AI ✨</p>
</div>
""", unsafe_allow_html=True)

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    # In voice-only mode, skip displaying text for assistant messages
    if not (st.session_state.voice_only_mode and message["role"] == "assistant"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display audio player for assistant messages (outside chat_message container)
    if message["role"] == "assistant":
        # Only generate TTS for the latest message to improve performance
        is_latest = i == len(st.session_state.messages) - 1

        if is_latest:
            audio_data = generate_tts_audio(message["content"], i)
            if audio_data:
                # Always auto-play the latest message
                st.audio(audio_data, format='audio/mp3', autoplay=True)

# Voice input section
st.markdown("""
<div style='background: rgba(255, 255, 255, 0.15); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;'>
    <h3 style='color: white; margin-top: 0;'>🎤 Voice Input</h3>
    <p style='color: rgba(255, 255, 255, 0.9); margin-bottom: 1rem;'>Click the microphone to record your message</p>
</div>
""", unsafe_allow_html=True)
audio_bytes = audio_recorder(
    text="",
    recording_color="#e74c3c",
    neutral_color="#3498db",
    icon_name="microphone",
    icon_size="2x",
    key="audio_recorder"
)

# Check if we have new audio and we're not currently processing
if audio_bytes:
    # Only process if this is different from the last recording
    if audio_bytes != st.session_state.last_audio_bytes:
        # Store this recording to prevent reprocessing
        st.session_state.last_audio_bytes = audio_bytes

        with st.spinner("Transcribing audio..."):
            transcribed_text = transcribe_audio(audio_bytes)

        if transcribed_text:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": transcribed_text})

            # Generate AI response without displaying (will be shown after rerun)
            with st.spinner("Generating response..."):
                ai_response = generate_ai_response_stream(transcribed_text)

            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

            # Rerun to display the new messages
            st.rerun()
else:
    # No audio - reset to allow new recordings
    if st.session_state.last_audio_bytes is not None:
        st.session_state.last_audio_bytes = None

st.markdown("""
<div style='background: rgba(255, 255, 255, 0.15); padding: 1.5rem; border-radius: 15px; margin: 2rem 0 1rem 0;'>
    <h3 style='color: white; margin-top: 0;'>⌨️ Text Input</h3>
    <p style='color: rgba(255, 255, 255, 0.9); margin-bottom: 0;'>Or type your message below</p>
</div>
""", unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate AI response without displaying (will be shown after rerun)
    with st.spinner("Generating response..."):
        ai_response = generate_ai_response_stream(prompt)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.rerun()
