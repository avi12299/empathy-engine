# 🎙️ The Empathy Engine

**AI Hackathon Challenge 1: Giving AI a Human Voice**  
*Theme: AI Beyond Words: Creative Synthesis & Interaction*

## 📋 Project Description

The Empathy Engine is an intelligent Text-to-Speech (TTS) system that dynamically modulates vocal characteristics based on detected emotions in the input text. Unlike traditional robotic TTS systems, this application bridges the gap between text-based sentiment and expressive, human-like audio output by analyzing emotional context and adjusting voice parameters accordingly.

### Key Capabilities:
- **Emotion Detection**: Analyzes text sentiment, keywords, and punctuation patterns
- **Dynamic Voice Modulation**: Adjusts speaking rate and volume based on emotional context
- **Intensity Scaling**: Emotional strength affects the degree of voice parameter changes
- **Interactive Web Interface**: User-friendly Streamlit application with real-time feedback
- **Audio Generation & Download**: Creates playable WAV files with emotional speech

## 🚀 Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd empathy-engine
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv empathy_env
source empathy_env/bin/activate  # On Windows: empathy_env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
```
streamlit>=1.28.0
pyttsx3>=2.90
textblob>=0.17.1
```

### Step 4: Initialize TextBlob (First Time Only)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

### Step 5: Run the Application
```bash
streamlit empathy_engine.py
```

The application will open in your default web browser at `http://localhost:8501`

## 💻 How to Use

1. **Launch the App**: Run the Streamlit command above
2. **Enter Text**: Type or paste your text in the main text area
3. **Quick Demo**: Use sidebar buttons for pre-configured emotional text samples
4. **Generate Speech**: Click "🎙️ Generate Emotional Speech" button
5. **Review Analysis**: View detected emotion, intensity, and vocal parameters
6. **Listen**: Play the generated audio directly in the browser
7. **Download**: Save the audio file for external use

### Sample Texts to Try:
- **Positive**: "This is absolutely fantastic news! I'm so excited!"
- **Negative**: "I'm really frustrated with this situation. This is terrible."
- **Neutral**: "The weather today is partly cloudy with a chance of rain."

## 🧠 Design Choices & Technical Implementation

### Emotion Detection Logic

The system employs a multi-layered approach to emotion analysis:

1. **Sentiment Polarity Analysis**: Uses TextBlob to calculate sentiment polarity (-1.0 to +1.0)
2. **Keyword Detection**: Scans for emotional trigger words to enhance accuracy
3. **Punctuation Analysis**: Exclamation marks increase emotional intensity
4. **Threshold Classification**: Maps polarity to three categories:
   - **Positive**: polarity > 0.3 (Happy/Enthusiastic)
   - **Negative**: polarity < -0.3 (Frustrated/Subdued)  
   - **Neutral**: -0.3 ≤ polarity ≤ 0.3 (Calm/Balanced)

### Emotion-to-Voice Parameter Mapping

Each emotion category has distinct vocal characteristics:

| Emotion | Base Rate (WPM) | Base Volume | Modulation Logic |
|---------|----------------|-------------|-------------------|
| **Positive** | 200 | 90% | Faster speech, higher volume with intensity |
| **Negative** | 150 | 70% | Slower speech, lower volume with intensity |
| **Neutral** | 175 | 80% | Balanced parameters, minimal variation |

### Intensity Scaling Algorithm

The system calculates emotional intensity (0.0-1.0) and applies dynamic scaling:

```python
# Positive emotion scaling
rate = 175 + (intensity × 50)  # Range: 175-225 WPM
volume = 0.8 + (intensity × 0.2)  # Range: 80%-100%

# Negative emotion scaling  
rate = 175 - (intensity × 40)  # Range: 135-175 WPM
volume = 0.8 - (intensity × 0.2)  # Range: 60%-80%
```

### Technical Architecture

- **Frontend**: Streamlit web framework with custom CSS styling
- **TTS Engine**: pyttsx3 for cross-platform speech synthesis
- **Emotion Analysis**: TextBlob sentiment analysis with keyword enhancement
- **Audio Processing**: WAV file generation with temporary file management
- **State Management**: Streamlit session state for consistent user experience

## 🎯 Core Requirements Fulfilled

✅ **Text Input**: Accepts string input via web interface  
✅ **Emotion Detection**: Classifies into Positive, Negative, and Neutral categories  
✅ **Vocal Parameter Modulation**: Dynamically adjusts Rate and Volume parameters  
✅ **Emotion-to-Voice Mapping**: Clear algorithmic mapping with intensity scaling  
✅ **Audio Output**: Generates playable WAV files  

## 🌟 Bonus Features Implemented

✅ **Granular Emotions**: Enhanced detection with emotional keywords and intensity  
✅ **Intensity Scaling**: Emotional strength affects degree of voice modulation  
✅ **Web Interface**: Complete Streamlit UI with real-time audio playback  
✅ **Advanced Features**: Download functionality, demo texts, and visual feedback  

## 🏗️ Project Structure

```
empathy-engine/
├── empathy_engine.py       # Main Streamlit UI application
├── requirements.txt       # Python dependencies
├── README.md             # This file
```

## 🔧 Troubleshooting

**Audio Not Playing?**
- Ensure your browser supports HTML5 audio
- Check system audio settings and volume levels
- Try different browsers (Chrome, Firefox recommended)

**TTS Engine Issues?**
- On Linux: `sudo apt-get install espeak espeak-data libespeak-dev`
- On macOS: TTS should work out of the box
- On Windows: Ensure SAPI is available

**Installation Problems?**
- Update pip: `pip install --upgrade pip`
- Install Visual C++ Build Tools (Windows only)
- Use conda instead of pip if issues persist

## 📈 Future Enhancements

- Integration with advanced emotion models (Hugging Face transformers)
- SSML support for fine-grained speech control  
- Multiple voice selection and language support
- Real-time emotion visualization and waveform display
- API endpoint development for programmatic access

## 👥 Team & Acknowledgments

Developed for the AI Hackathon "AI Beyond Words: Creative Synthesis & Interaction"  
Challenge 1: The Empathy Engine - Giving AI a Human Voice

**Technologies Used:**
- Python 3.12
- Streamlit (Web Framework)
- pyttsx3 (Text-to-Speech)
- TextBlob (Sentiment Analysis)
- HTML/CSS (UI Styling)

---
