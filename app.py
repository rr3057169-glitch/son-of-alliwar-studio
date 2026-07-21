import streamlit as st
import asyncio
import edge_tts
import requests
import tempfile
import os

# Page Setup
st.set_page_config(page_title="Son Of Alliwar Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Son Of Alliwar Studio")
st.subheader("Simple & Fast Voice Generator")

# Mode Selection
engine_choice = st.radio(
    "🎙️ **मोड निवडा (Select Engine):**",
    ["🆓 Free Engine (19+ Languages)", "💎 Premium Engine (ElevenLabs)"],
    horizontal=True
)

st.divider()

# Session state initialization for + / - buttons
if "speed" not in st.session_state:
    st.session_state.speed = 0
if "pitch" not in st.session_state:
    st.session_state.pitch = 0

# Helper function for Async Edge TTS with better error handling
def text_to_speech(text, voice_code, rate_str, pitch_str):
    async def _gen():
        communicate = edge_tts.Communicate(text, voice_code, rate=rate_str, pitch=pitch_str)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            path = tmp_file.name
        await communicate.save(path)
        return path

    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                res = pool.submit(asyncio.run, _gen()).result()
                return res
        else:
            return asyncio.run(_gen())
    except Exception as e:
        raise Exception(f"TTS Generation Failed: {str(e)}")

# Language Database
voice_db = {
    # 🇮🇳 Indian Languages
    "मराठी (Marathi)": {"Male": "mr-IN-MadhavNeural", "Female": "mr-IN-AarohiNeural"},
    "हिंदी (Hindi)": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
    "English (India)": {"Male": "en-IN-PrabhatNeural", "Female": "en-IN-NeerjaNeural"},
    "தமிழ் (Tamil)": {"Male": "ta-IN-ValluvarNeural", "Female": "ta-IN-PallaviNeural"},
    "తెలుగు (Telugu)": {"Male": "te-IN-MohanNeural", "Female": "te-IN-ShrutiNeural"},
    "ಕನ್ನಡ (Kannada)": {"Male": "kn-IN-GaganNeural", "Female": "kn-IN-SapnaNeural"},
    "മലയാളം (Malayalam)": {"Male": "ml-IN-MidhunNeural", "Female": "ml-IN-SobhanaNeural"},
    "ગુજરાતી (Gujarati)": {"Male": "gu-IN-NiranjanNeural", "Female": "gu-IN-DhwaniNeural"},
    "বাংলা (Bengali)": {"Male": "bn-IN-BashkarNeural", "Female": "bn-IN-TanishaaNeural"},
    "ਪੰਜਾਬੀ (Punjabi)": {"Male": "pa-IN-OjasNeural", "Female": "pa-IN-VaaniNeural"},
    "اردو (Urdu)": {"Male": "ur-IN-SalmanNeural", "Female": "ur-IN-GulNeural"},
    "ଓଡ଼ିଆ (Odia)": {"Male": "or-IN-SubhasiniNeural", "Female": "or-IN-SubhasiniNeural"},
    
    # 🌍 Foreign Languages
    "English (US)": {"Male": "en-US-GuyNeural", "Female": "en-US-AriaNeural"},
    "English (UK)": {"Male": "en-GB-RyanNeural", "Female": "en-GB-SoniaNeural"},
    "Español (Spanish)": {"Male": "es-ES-AlvaroNeural", "Female": "es-ES-ElviraNeural"},
    "Français (French)": {"Male": "fr-FR-HenriNeural", "Female": "fr-FR-DeniseNeural"},
    "Deutsch (German)": {"Male": "de-DE-ConradNeural", "Female": "de-DE-KatjaNeural"},
    "日本語 (Japanese)": {"Male": "ja-JP-KeitaNeural", "Female": "ja-JP-NanamiNeural"},
    "العربية (Arabic)": {"Male": "ar-SA-HamedNeural", "Female": "ar-SA-ZariyahNeural"}
}

# ==========================================
# 🆓 1. FREE ENGINE MODE
# ==========================================
if "Free Engine" in engine_choice:
    col_lang, col_gender = st.columns(2)
    with col_lang:
        selected_lang = st.selectbox("🌐 भाषा निवडा:", list(voice_db.keys()))
    with col_gender:
        selected_gender = st.selectbox("🎭 पात्र निवडा:", ["Male (पुरुष)", "Female (स्त्री)"])

    # Pitch & Speed Controls with + and - buttons
    st.write("---")
    st.write("⚙️ **Voice Controls:**")
    
    col_sp_btn1, col_sp_val, col_sp_btn2 = st.columns([1, 2, 1])
    with col_sp_btn1:
        if st.button("➖ Speed", key="sp_down"):
            st.session_state.speed = max(-50, st.session_state.speed - 5)
    with col_sp_val:
        st.markdown(f"<h4 style='text-align: center;'>⚡ Speed: {st.session_state.speed}%</h4>", unsafe_allow_html=True)
    with col_sp_btn2:
        if st.button("➕ Speed", key="sp_up"):
            st.session_state.speed = min(50, st.session_state.speed + 5)

    col_p_btn1, col_p_val, col_p_btn2 = st.columns([1, 2, 1])
    with col_p_btn1:
        if st.button("➖ Pitch", key="p_down"):
            st.session_state.pitch = max(-20, st.session_state.pitch - 2)
    with col_p_val:
        st.markdown(f"<h4 style='text-align: center;'>🎼 Pitch: {st.session_state.pitch}Hz</h4>", unsafe_allow_html=True)
    with col_p_btn2:
        if st.button("➕ Pitch", key="p_up"):
            st.session_state.pitch = min(20, st.session_state.pitch + 2)

    st.write("---")

    rate_str = f"{'+' if st.session_state.speed >= 0 else ''}{st.session_state.speed}%"
    pitch_str = f"{'+' if st.session_state.pitch >= 0 else ''}{st.session_state.pitch}Hz"

    gender_key = "Male" if "Male" in selected_gender else "Female"
    voice_code = voice_db[selected_lang][gender_key]

    text_input = st.text_area("📝 मजकूर लिहा:", height=150, placeholder="इथे तुमचा मजकूर टाका...")

    if st.button("🔊 Generate Voice", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ कृपया मजकूर लिहा!")
        else:
            with st.spinner("✨ आवाज तयार होत आहे..."):
                try:
                    audio_path = text_to_speech(text_input, voice_code, rate_str, pitch_str)
                    with open(audio_path, "rb") as f:
                        audio_data = f.read()
                        st.success("🎉 आवाज तयार झाला!")
                        st.audio(audio_data, format="audio/mp3")
                        st.download_button("📥 MP3 Download करा", audio_data, file_name="alliwar_voice.mp3", mime="audio/mp3")
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                except Exception as e:
                    st.error(f" एरर आली: कृपया मजकूर थोडा लहान करा किंवा पुन्हा प्रयत्न करा. ({str(e)})")

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
