
"""
The Empathy Engine - AI Hackathon Challenge 1
Interactive web interface for the emotional TTS system
"""


import streamlit as st
import pyttsx3
import os
import time
import base64
from textblob import TextBlob
from typing import Dict, Tuple
import tempfile
import threading
import queue

class EmpathyEngineStreamlit:
    def __init__(self):
        """Initialize the Empathy Engine with TTS engine and emotion mappings."""
        if 'engine' not in st.session_state:
            st.session_state.engine = pyttsx3.init()
            
            # Get available voices
            voices = st.session_state.engine.getProperty('voices')
            if voices:
                st.session_state.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        
        self.engine = st.session_state.engine
        
        # Emotion to voice parameter mapping
        self.emotion_mapping = {
            'positive': {
                'rate': 200,
                'volume': 0.9,
                'description': '😊 Happy & Enthusiastic',
                'color': '#4CAF50'
            },
            'negative': {
                'rate': 150,
                'volume': 0.7,
                'description': '😔 Frustrated & Subdued',
                'color': '#F44336'
            },
            'neutral': {
                'rate': 175,
                'volume': 0.8,
                'description': '😐 Calm & Balanced',
                'color': '#FF9800'
            }
        }
    
    def detect_emotion(self, text: str) -> Tuple[str, float]:
        """Detect emotion from text using enhanced analysis."""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Enhanced emotion detection with intensity
        if polarity > 0.3:
            emotion = 'positive'
            intensity = min(polarity * 2, 1.0)
        elif polarity < -0.3:
            emotion = 'negative'
            intensity = min(abs(polarity) * 2, 1.0)
        else:
            emotion = 'neutral'
            intensity = 0.5
            
        # Check for emotional keywords
        positive_words = ['amazing', 'fantastic', 'wonderful', 'excellent', 'great', 'awesome', 'love', 'excited', 'thrilled', 'delighted', 'happy', 'joy']
        negative_words = ['terrible', 'awful', 'horrible', 'frustrated', 'angry', 'sad', 'disappointed', 'worried', 'concerned', 'hate', 'upset']
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in positive_words):
            emotion = 'positive'
            intensity = max(intensity, 0.8)
        elif any(word in text_lower for word in negative_words):
            emotion = 'negative'
            intensity = max(intensity, 0.8)
            
        # Check for exclamation marks
        exclamation_count = text.count('!')
        if exclamation_count > 0:
            intensity = min(intensity + (exclamation_count * 0.2), 1.0)
            
        return emotion, intensity
    
    def apply_vocal_modulation(self, emotion: str, intensity: float):
        """Apply vocal parameter modulation based on emotion and intensity."""
        base_params = self.emotion_mapping[emotion].copy()
        
        # Intensity scaling
        if emotion == 'positive':
            base_params['rate'] = int(175 + (intensity * 50))
            base_params['volume'] = 0.8 + (intensity * 0.2)
        elif emotion == 'negative':
            base_params['rate'] = int(175 - (intensity * 40))
            base_params['volume'] = 0.8 - (intensity * 0.2)
        else:
            base_params['rate'] = 175
            base_params['volume'] = 0.8
            
        # Apply settings to TTS engine
        self.engine.setProperty('rate', base_params['rate'])
        self.engine.setProperty('volume', base_params['volume'])
        
        return base_params
    
    def generate_speech(self, text: str) -> Dict:
        """Generate emotional speech from text."""
        # Detect emotion and intensity
        emotion, intensity = self.detect_emotion(text)
        
        # Apply vocal modulation
        vocal_params = self.apply_vocal_modulation(emotion, intensity)
        
        # Generate unique filename
        timestamp = int(time.time())
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, f"empathy_output_{timestamp}.wav")
        
        try:
            # Generate speech
            self.engine.save_to_file(text, output_file)
            self.engine.runAndWait()
            
            # Wait a moment for file to be written
            time.sleep(0.5)
            
            success = os.path.exists(output_file)
        except Exception as e:
            success = False
            st.error(f"TTS Error: {str(e)}")
        
        result = {
            'text': text,
            'emotion': emotion,
            'intensity': round(intensity, 2),
            'vocal_parameters': vocal_params,
            'audio_file': output_file if success else None,
            'success': success
        }
        
        return result

def get_audio_html(audio_file: str) -> str:
    """Generate HTML for audio player."""
    if not os.path.exists(audio_file):
        return ""
    
    with open(audio_file, "rb") as audio:
        audio_bytes = audio.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
    return f"""
    <audio controls style="width: 100%;">
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
        Your browser does not support the audio element.
    </audio>
    """

def main():
    # Page config
    st.set_page_config(
        page_title="🎙️ The Empathy Engine",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    .emotion-card {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .demo-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎙️ The Empathy Engine</h1>
        <p>Give AI a Human Voice with Emotional Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize the engine
    if 'empathy_engine' not in st.session_state:
        st.session_state.empathy_engine = EmpathyEngineStreamlit()
    
    engine = st.session_state.empathy_engine
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Demo texts
        st.subheader("📋 Quick Demo Texts")
        demo_texts = {
            "😊 Super Excited": "This is absolutely fantastic news! I'm so excited about this opportunity!",
            "😤 Frustrated": "I'm really frustrated with this situation. This is not working at all.",
            "😐 Neutral": "The weather today is partly cloudy with a chance of rain.",
            "🤩 Extremely Happy": "OH MY GOD! This is the best day ever! I can't believe this is happening!",
            "😟 Concerned": "I'm deeply concerned about the recent developments. This is quite troubling."
        }
        
        for label, text in demo_texts.items():
            if st.button(label, key=f"demo_{label}"):
                st.session_state.selected_text = text
        
        st.markdown("---")
        st.markdown("### 🎯 How It Works")
        st.markdown("""
        1. **Text Analysis**: Analyzes sentiment, keywords, and punctuation
        2. **Emotion Detection**: Classifies into Positive, Negative, or Neutral
        3. **Intensity Scaling**: Measures emotional strength (0.0-1.0)
        4. **Voice Modulation**: Adjusts rate and volume parameters
        5. **Audio Generation**: Creates expressive speech output
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Text Input")
        
        # Text input
        default_text = st.session_state.get('selected_text', "Enter your text here to hear it with emotional voice modulation!")
        text_input = st.text_area(
            "Enter your text:",
            value=default_text,
            height=120,
            help="Type any text and the system will detect its emotion and adjust the voice accordingly."
        )
        
        # Generate button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            generate_btn = st.button("🎙️ Generate Emotional Speech", type="primary", use_container_width=True)
        
        # Process text when button is clicked
        if generate_btn and text_input.strip():
            with st.spinner("🔍 Analyzing emotion and generating speech..."):
                result = engine.generate_speech(text_input.strip())
                st.session_state.last_result = result
        
        # Display results
        if hasattr(st.session_state, 'last_result') and st.session_state.last_result:
            result = st.session_state.last_result
            
            st.header("📊 Analysis Results")
            
            # Emotion display
            emotion_info = engine.emotion_mapping[result['emotion']]
            st.markdown(f"""
            <div class="emotion-card" style="border-left-color: {emotion_info['color']};">
                <h3 style="color: {emotion_info['color']}; margin: 0;">
                    {emotion_info['description']}
                </h3>
                <p style="margin: 0.5rem 0 0 0;">
                    <strong>Emotion:</strong> {result['emotion'].title()} | 
                    <strong>Intensity:</strong> {result['intensity']}/1.0
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Vocal parameters
            st.subheader("🎛️ Vocal Parameters")
            param_col1, param_col2 = st.columns(2)
            
            with param_col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h4>🏃‍♂️ Speaking Rate</h4>
                    <h2>{result['vocal_parameters']['rate']} WPM</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with param_col2:
                volume_percent = int(result['vocal_parameters']['volume'] * 100)
                st.markdown(f"""
                <div class="metric-container">
                    <h4>🔊 Volume Level</h4>
                    <h2>{volume_percent}%</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Audio output
            if result['success'] and result['audio_file']:
                st.header("🔊 Audio Output")
                st.markdown("**Generated emotional speech:**")
                audio_html = get_audio_html(result['audio_file'])
                if audio_html:
                    st.markdown(audio_html, unsafe_allow_html=True)
                    
                    # Download link
                    with open(result['audio_file'], "rb") as file:
                        st.download_button(
                            label="📥 Download Audio File",
                            data=file.read(),
                            file_name=f"empathy_speech_{int(time.time())}.wav",
                            mime="audio/wav"
                        )
                else:
                    st.error("Could not load audio file for playback.")
            else:
                st.error("❌ Failed to generate audio. Please try again.")
    
    with col2:
        st.header("📈 Emotion Guide")
        
        # Emotion mapping guide
        for emotion, params in engine.emotion_mapping.items():
            st.markdown(f"""
            <div class="demo-card">
                <h4 style="color: {params['color']}; margin: 0 0 0.5rem 0;">
                    {params['description']}
                </h4>
                <p style="margin: 0; font-size: 0.9em;">
                    <strong>Rate:</strong> {params['rate']} WPM<br>
                    <strong>Volume:</strong> {int(params['volume']*100)}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.header("🎯 Features")
        features = [
            "🎭 **3 Emotion Categories**: Positive, Negative, Neutral",
            "📊 **Intensity Scaling**: Emotional strength affects voice changes",
            "🔍 **Smart Detection**: Analyzes sentiment, keywords & punctuation",
            "🎛️ **Real-time Modulation**: Dynamic rate and volume adjustment",
            "🔊 **Instant Playback**: Hear results immediately",
            "📥 **Download Audio**: Save generated speech files"
        ]
        
        for feature in features:
            st.markdown(feature)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>🏆 AI Hackathon Challenge 1</strong><br>
        "AI Beyond Words: Creative Synthesis & Interaction"</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()