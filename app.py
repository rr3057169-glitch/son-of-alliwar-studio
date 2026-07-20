import streamlit as st
import requests

# Page Setup
st.set_page_config(page_title="Son Of Alliwar Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Son Of Alliwar Studio")
st.subheader("Global AI Voice Generator (ElevenLabs)")

# ElevenLabs API Key Input Box
api_key = st.text_input("🔑 तुमची ElevenLabs API Key टाका:", type="password", placeholder="xi-api-key...")

# Check API Limit Feature
if api_key:
    if st.button("📊 API Limit / Remaining Characters तपासा"):
        headers = {"xi-api-key": api_key}
        try:
            response = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers=headers)
            if response.status_code == 200:
                data = response.json()
                used = data.get("character_count", 0)
                limit = data.get("character_limit", 10000)
                remaining = limit - used
                st.info(f"💡 **शिल्लक कॅरेक्टर्स:** {remaining} / {limit} (वापरलेले: {used})")
            else:
                st.error("❌ API Key चुकीची आहे किंवा कनेक्ट होत नाहीये.")
        except Exception as e:
            st.error(f"कनेक्शन एरर: {str(e)}")

st.divider()

# Text Script Input Box
text_input = st.text_area(
    "📝 तुमची स्क्रिप्ट / मजकूर लिहा:", 
    height=150, 
    placeholder="मराठी, हिंदी, English, Spanish, French किंवा कोणत्याही आंतरराष्ट्रीय भाषेत टाईप करा..."
)

# ElevenLabs Multilingual Voices
voices = {
    "Adam (Deep Male - Best for Stories)": "pNInz6obpgDQGcFmJgQb",
    "Rachel (Calm Female - Professional)": "21m00Tcm4TlvDq8ikWAM",
    "Domi (Energetic Female)": "AZnzlk1XvdvUeBnXmlld",
    "Bella (Soft Female)": "EXAVITQu4vr4xnSDxMaL",
    "Antoni (Versatile Male)": "ErXwobaYiN019PkySvjV"
}

selected_voice_name = st.selectbox("🎙️ आवाज (Voice) निवडा:", list(voices.keys()))
selected_voice_id = voices[selected_voice_name]

# Function to call ElevenLabs API
def generate_elevenlabs_voice(text, voice_id, key):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2", # Supports Marathi, Hindi, English & Global Languages
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content, None
        else:
            return None, f"API Error ({response.status_code}): {response.text}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

# Generate Button
if st.button("🔊 Generate Voice (आवाज तयार करा)", type="primary"):
    if not api_key:
        st.error("⚠️ कृपया तुमची ElevenLabs API Key टाका!")
    elif not text_input.strip():
        st.warning("⚠️ कृपया आधी काहीतरी मजकूर लिहा!")
    else:
        with st.spinner("✨ ElevenLabs AI आवाज तयार करत आहे..."):
            audio_data, error_msg = generate_elevenlabs_voice(text_input, selected_voice_id, api_key)
            
            if audio_data:
                st.success("🎉 आवाज यशस्वीपणे तयार झाला आहे!")
                st.audio(audio_data, format="audio/mp3")
                
                # Download Button
                st.download_button(
                    label="📥 MP3 Audio Download करा",
                    data=audio_data,
                    file_name="alliwar_studio_voice.mp3",
                    mime="audio/mp3"
                )
            else:
                st.error(error_msg)
