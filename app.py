import streamlit as st
import asyncio
import edge_tts
import requests
import tempfile
import os

# Page Setup
st.set_page_config(page_title="Son Of Alliwar Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Son Of Alliwar Studio")
st.subheader("All-in-One Voice Generator (12 Indian + Foreign Languages)")

# Mode Selection
engine_choice = st.radio(
    "🎙️ **व्हॉईस इंजिन निवडा (Select Voice Mode):**",
    ["🆓 Free Mode (Unlimited - Pitch, Speed & 12 Languages)", "💎 Premium Mode (ElevenLabs - Multilingual)"],
    horizontal=True
)

st.divider()

# ==========================================
# 🆓 FREE UNLIMITED MODE (Edge-TTS)
# ==========================================
if "Free Mode" in engine_choice:
    st.success("✅ **Free Unlimited Mode:** १२ भारतीय भाषा + फॉरेन भाषा, Male/Female पात्रे, Pitch आणि Speed कंट्रोल!")

    # 1. Language Selection
    lang_map = {
        "मराठी (Marathi)": {"Male": "mr-IN-MadhavNeural", "Female": "mr-IN-AarohiNeural"},
        "हिंदी (Hindi)": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
        "English (India)": {"Male": "en-IN-PrabhatNeural", "Female": "en-IN-NeerjaNeural"},
        "தமிழ் (Tamil)": {"Male": "ta-IN-ValluvarNeural", "Female": "ta-IN-PallaviNeural"},
        "తెలుగు (Telugu)": {"Male": "te-IN-MohanNeural", "Female": "te-IN-ShrutiNeural"},
        "ಕನ್ನಡ (Kannada)": {"Male": "kn-IN-GaganNeural", "Female": "kn-IN-SapnaNeural"},
        "മലയാളം (Malayalam)": {"Male": "ml-IN-MidhunNeural", "Female": "ml-IN-SobhanaNeural"},
        "ગુજરાતી (Gujarati)": {"Male": "gu-IN-NiranjanNeural", "Female": "gu-IN-DhwaniNeural"},
        "বাংলা (Bengali)": {"Male": "bn-IN-BashkarNeural", "Female": "bn-IN-TanishaaNeural"},
        "ਪੰਜਾਬੀ (Punjabi)": {"Male": "pa-IN-VaaniNeural", "Female": "pa-IN-VaaniNeural"},
        "اردو (Urdu)": {"Male": "ur-IN-GulNeural", "Female": "ur-IN-GulNeural"},
        "ଓଡ଼ିଆ (Odia)": {"Male": "or-IN-SubhasiniNeural", "Female": "or-IN-SubhasiniNeural"},
        "English (US)": {"Male": "en-US-GuyNeural", "Female": "en-US-AriaNeural"},
        "Spanish (Español)": {"Male": "es-ES-AlvaroNeural", "Female": "es-ES-ElviraNeural"},
        "French (Français)": {"Male": "fr-FR-HenriNeural", "Female": "fr-FR-DeniseNeural"},
        "German (Deutsch)": {"Male": "de-DE-ConradNeural", "Female": "de-DE-KlarissaNeural"},
        "Japanese (日本語)": {"Male": "ja-JP-KeitaNeural", "Female": "ja-JP-NanamiNeural"},
        "Arabic (العربية)": {"Male": "ar-SA-HamedNeural", "Female": "ar-SA-ZariyahNeural"}
    }

    col_lang, col_gender = st.columns(2)
    with col_lang:
        selected_lang = st.selectbox("🌐 भाषा निवडा (Language):", list(lang_map.keys()))
    
    with col_gender:
        selected_gender = st.selectbox("🎭 पात्र / लिंग (Gender):", ["Male (पुरुष)", "Female (स्त्री)"])

    gender_key = "Male" if "Male" in selected_gender else "Female"
    voice_code = lang_map[selected_lang][gender_key]

    # 2. Controls: Speed & Pitch
    col_speed, col_pitch = st.columns(2)
    with col_speed:
        speed_val = st.slider("⚡ आवाजाचा वेग (Speed):", min_value=-50, max_value=50, value=0, step=5, format="%d%%")
        speed_str = f"{speed_val:+d}%"

    with col_pitch:
        pitch_val = st.slider("🎵 आवाजाचा चढाव/उतार (Pitch):", min_value=-50, max_value=50, value=0, step=5, format="%dHz")
        pitch_str = f"{pitch_val:+d}Hz"

    # 3. Text Area
    text_input = st.text_area("📝 तुमची स्क्रिप्ट / मजकूर लिहा:", height=150, placeholder="निवडलेल्या भाषेत इथे मजकूर लिहा...")

    async def generate_edge_audio(text, voice, rate, pitch):
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            output_filename = tmp_file.name
        await communicate.save(output_filename)
        return output_filename

    if st.button("🔊 Generate Free Voice", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ कृपया आधी मजकूर लिहा!")
        else:
            with st.spinner("✨ मोफत आवाज तयार होत आहे..."):
                try:
                    audio_path = asyncio.run(generate_edge_audio(text_input, voice_code, speed_str, pitch_str))
                    
                    with open(audio_path, "rb") as f:
                        audio_data = f.read()
                        st.success("🎉 आवाज तयार झाला!")
                        st.audio(audio_data, format="audio/mp3")
                        st.download_button("📥 MP3 Download करा", audio_data, file_name="alliwar_studio_free.mp3", mime="audio/mp3")
                    
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ==========================================
# 💎 PREMIUM ELEVENLABS MODE
# ==========================================
else:
    st.info("💎 **Premium Mode:** ElevenLabs Multilingual v2 Engine (All 12 Indian & Foreign Languages Supported).")
    
    api_key = st.text_input("🔑 तुमची ElevenLabs API Key टाका:", type="password", placeholder="xi-api-key...")
    
    if api_key:
        if st.button("📊 API Limit तपासा"):
            headers = {"xi-api-key": api_key}
            try:
                res = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    used = data.get("character_count", 0)
                    limit = data.get("character_limit", 10000)
                    st.info(f"💡 **शिल्लक कॅरेक्टर्स:** {limit - used} / {limit}")
                else:
                    st.error("❌ API Key चुकीची आहे.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.divider()

    eleven_voices = {
        "Adam (Deep Male - Deep Stories)": "pNInz6obpgDQGcFmJgQb",
        "Rachel (Calm Female - Professional)": "21m00Tcm4TlvDq8ikWAM",
        "Domi (Energetic Female)": "AZnzlk1XvdvUeBnXmlld",
        "Bella (Soft Female)": "EXAVITQu4vr4xnSDxMaL",
        "Antoni (Versatile Male)": "ErXwobaYiN019PkySvjV"
    }

    selected_ev = st.selectbox("🎙️ ElevenLabs पात्र निवडा:", list(eleven_voices.keys()))
    ev_id = eleven_voices[selected_ev]

    text_input = st.text_area("📝 स्क्रिप्ट लिहा (कोणत्याही भाषेत):", height=150, placeholder="मराठी, हिंदी, English किंवा इतर कोणत्याही भाषेत लिहा...")

    if st.button("🔊 Generate Premium Voice", type="primary"):
        if not api_key:
            st.error("⚠️ कृपया आधी API Key टाका!")
        elif not text_input.strip():
            st.warning("⚠️ कृपया मजकूर लिहा!")
        else:
            with st.spinner("✨ ElevenLabs नॅचरल आवाज तयार करत आहे..."):
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{ev_id}"
                headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": api_key}
                data = {
                    "text": text_input,
                    "model_id": "eleven_multilingual_v2"
                }
                
                res = requests.post(url, json=data, headers=headers)
                if res.status_code == 200:
                    st.success("🎉 Premium आवाज तयार झाला!")
                    st.audio(res.content, format="audio/mp3")
                    st.download_button("📥 MP3 Download करा", res.content, file_name="alliwar_studio_premium.mp3", mime="audio/mp3")
                else:
                    st.error(f"API Error: {res.text}")
