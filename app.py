import streamlit as st
from gtts import gTTS
import tempfile
import os

# Page Setup
st.set_page_config(page_title="Son Of Alliwar Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Son Of Alliwar Studio")
st.subheader("Fast & Reliable Voice Generator")

# Mode Selection
engine_choice = st.radio(
    "🎙️ **मोड निवडा (Select Engine):**",
    ["🆓 Free Engine (Google TTS)", "💎 Premium Engine (ElevenLabs)"],
    horizontal=True
)

st.divider()

# Language Database for gTTS
lang_codes = {
    "मराठी (Marathi)": "mr",
    "हिंदी (Hindi)": "hi",
    "English (India)": "en",
    "English (US)": "en",
    "English (UK)": "en",
    "தமிழ் (Tamil)": "ta",
    "తెలుగు (Telugu)": "te",
    "ಕನ್ನಡ (Kannada)": "kn",
    "മലയാളം (Malayalam)": "ml",
    "ગુજરાતી (Gujarati)": "gu",
    "বাংলা (Bengali)": "bn",
    "ਪੰਜਾਬੀ (Punjabi)": "pa",
    "Español (Spanish)": "es",
    "Français (French)": "fr",
    "Deutsch (German)": "de",
    "日本語 (Japanese)": "ja",
    "العربية (Arabic)": "ar"
}

# ==========================================
# 🆓 1. FREE ENGINE MODE (gTTS)
# ==========================================
if "Free Engine" in engine_choice:
    selected_lang = st.selectbox("🌐 भाषा निवडा:", list(lang_codes.keys()))
    text_input = st.text_area("📝 मजकूर लिहा:", height=150, placeholder="इथे तुमचा मजकूर टाका...")

    if st.button("🔊 Generate Voice", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ कृपया मजकूर लिहा!")
        else:
            with st.spinner("✨ आवाज तयार होत आहे..."):
                try:
                    lang_code = lang_codes[selected_lang]
                    tts = gTTS(text=text_input, lang=lang_code, slow=False)
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                        temp_path = tmp_file.name
                    
                    tts.save(temp_path)
                    
                    with open(temp_path, "rb") as f:
                        audio_data = f.read()
                        st.success("🎉 आवाज तयार झाला!")
                        st.audio(audio_data, format="audio/mp3")
                        st.download_button("📥 MP3 Download करा", audio_data, file_name="alliwar_voice.mp3", mime="audio/mp3")
                    
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except Exception as e:
                    st.error(f"एरर आली: {str(e)}")

# ==========================================
# 💎 2. PREMIUM ENGINE (ELEVENLABS)
# ==========================================
else:
    api_key = st.text_input("🔑 ElevenLabs API Key:", type="password")
    
    eleven_voices = {
        "Adam (Deep Male)": "pNInz6obpgDQGcFmJgQb",
        "Josh (Young Male)": "TxGEqnscrfWFTf83CqRO",
        "Rachel (Calm Female)": "21m00Tcm4TlvDq8ikWAM",
        "Domi (Strong Female)": "AZnzlk1XvdvUeBnXmlld"
    }

    selected_ev = st.selectbox("🎙️ पात्र निवडा:", list(eleven_voices.keys()))
    ev_id = eleven_voices[selected_ev]
    text_input = st.text_area("📝 मजकूर लिहा:", height=150, placeholder="इथे तुमचा मजकूर टाका...")

    if st.button("🔊 Generate Premium Voice", type="primary"):
        if not api_key:
            st.error("⚠️ कृपया API Key टाका!")
        elif not text_input.strip():
            st.warning("⚠️ कृपया मजकूर लिहा!")
        else:
            with st.spinner("✨ ElevenLabs आवाज तयार करत आहे..."):
                import requests
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{ev_id}"
                headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": api_key}
                data = {"text": text_input, "model_id": "eleven_multilingual_v2"}
                
                res = requests.post(url, json=data, headers=headers)
                if res.status_code == 200:
                    st.success("🎉 Premium आवाज तयार झाला!")
                    st.audio(res.content, format="audio/mp3")
                    st.download_button("📥 MP3 Download करा", res.content, file_name="alliwar_premium.mp3", mime="audio/mp3")
                else:
                    st.error(f"API Error: {res.text}")
