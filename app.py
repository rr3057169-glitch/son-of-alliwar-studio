import streamlit as st
import asyncio
import edge_tts
import requests
import tempfile
import os

# Page Setup
st.set_page_config(page_title="Son Of Alliwar Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Son Of Alliwar Studio")
st.subheader("All-in-One Multi-Character Voice Generator")

# Mode Selection
engine_choice = st.radio(
    "🎙️ **व्हॉईस इंजिन निवडा (Select Voice Mode):**",
    [
        "🎭 Free Multi-Character Story Mode", 
        "💎 Premium Multi-Character (ElevenLabs)", 
        "🆓 Single Voice Free Mode", 
        "💎 Single Voice Premium Mode"
    ],
    horizontal=True
)

st.divider()

# ==========================================
# 🎭 1. FREE MULTI-CHARACTER STORY MODE
# ==========================================
if "Free Multi-Character" in engine_choice:
    st.success("✨ **Free Multi-Character Mode:** पुरुष आणि स्त्री संवादांची पूर्ण कथा एकाच वेळी बनवा!")
    
    col_l, col_m, col_f = st.columns(3)
    with col_l:
        lang_choice = st.selectbox("🌐 कथा भाषा (Language):", ["Marathi", "Hindi", "English (India)"])
    
    voice_db = {
        "Marathi": {"Male": "mr-IN-MadhavNeural", "Female": "mr-IN-AarohiNeural"},
        "Hindi": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
        "English (India)": {"Male": "en-IN-PrabhatNeural", "Female": "en-IN-NeerjaNeural"}
    }
    
    male_voice = voice_db[lang_choice]["Male"]
    female_voice = voice_db[lang_choice]["Female"]

    st.markdown("""
    💡 **फॉर्मॅट:**  
    `राजू: अरे तू कुठे चाललास?`  
    `सीमा: मी बाजारात चालले आहे.`
    """)

    story_text = st.text_area("📝 कथा / संवाद लिहा:", height=200, placeholder="राजू: अरे सीमा तू कुठे चाललीस?\nसीमा: मी बाजारात चालले आहे, तू पण येतोस का?")

    col_s, col_p = st.columns(2)
    with col_s:
        speed_val = st.slider("⚡ Speed:", -50, 50, 0, 5, format="%d%%")
        speed_str = f"{speed_val:+d}%"
    with col_p:
        pitch_val = st.slider("🎵 Pitch:", -50, 50, 0, 5, format="%dHz")
        pitch_str = f"{pitch_val:+d}Hz"

    async def generate_dialogue(text):
        lines = text.strip().split("\n")
        audio_files = []
        
        for line in lines:
            if not line.strip():
                continue
            
            current_voice = male_voice
            speaker_text = line.strip()

            if ":" in line:
                parts = line.split(":", 1)
                speaker_name = parts[0].strip().lower()
                speaker_text = parts[1].strip()

                if any(k in speaker_name for k in ["female", "girl", "woman", "स्त्री", "मुलगी", "सीमा", "पूजा", "अंकिता", "रिया", "राधा"]):
                    current_voice = female_voice

            if speaker_text:
                communicate = edge_tts.Communicate(speaker_text, current_voice, rate=speed_str, pitch=pitch_str)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_name = tmp_file.name
                await communicate.save(tmp_name)
                audio_files.append(tmp_name)

        combined_data = bytearray()
        for fpath in audio_files:
            with open(fpath, "rb") as f:
                combined_data.extend(f.read())
            if os.path.exists(fpath):
                os.remove(fpath)
                
        return combined_data

    if st.button("🔊 Generate Free Story Audio", type="primary"):
        if not story_text.strip():
            st.warning("⚠️ कृपया कथा लिहा!")
        else:
            with st.spinner("✨ पूर्ण कथेचा आवाज तयार होत आहे..."):
                try:
                    full_audio = asyncio.run(generate_dialogue(story_text))
                    st.success("🎉 Audio तयार झाला!")
                    st.audio(bytes(full_audio), format="audio/mp3")
                    st.download_button("📥 MP3 Download करा", bytes(full_audio), file_name="alliwar_free_story.mp3", mime="audio/mp3")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ==========================================
# 💎 2. PREMIUM MULTI-CHARACTER (ELEVENLABS)
# ==========================================
elif "Premium Multi-Character" in engine_choice:
    st.info("💎 **ElevenLabs Multi-Character Story Mode:** Adam (Male) आणि Rachel (Female) च्या आवाजात HD स्टोरी बनवा!")
    
    api_key = st.text_input("🔑 ElevenLabs API Key टाका:", type="password")

    st.markdown("""
    💡 **फॉर्मॅट:**  
    `राजू: अरे तू कुठे चाललास?`  
    `सीमा: मी बाजारात चालले आहे.`
    """)

    story_text = st.text_area("📝 कथा / संवाद लिहा:", height=200, placeholder="राजू: अरे सीमा तू कुठे चाललीस?\nसीमा: मी बाजारात चालले आहे, तू पण येतोस का?")

    eleven_male_id = "pNInz6obpgDQGcFmJgQb"    # Adam
    eleven_female_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel

    def generate_eleven_story(text, key):
        lines = text.strip().split("\n")
        combined_data = bytearray()

        for line in lines:
            if not line.strip():
                continue

            current_voice_id = eleven_male_id
            speaker_text = line.strip()

            if ":" in line:
                parts = line.split(":", 1)
                speaker_name = parts[0].strip().lower()
                speaker_text = parts[1].strip()

                if any(k in speaker_name for k in ["female", "girl", "woman", "स्त्री", "मुलगी", "सीमा", "पूजा", "अंकिता", "रिया", "राधा"]):
                    current_voice_id = eleven_female_id

            if speaker_text:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{current_voice_id}"
                headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": key}
                data = {"text": speaker_text, "model_id": "eleven_multilingual_v2"}
                
                res = requests.post(url, json=data, headers=headers)
                if res.status_code == 200:
                    combined_data.extend(res.content)
                else:
                    st.error(f"Error on line: {speaker_text} | Details: {res.text}")
                    return None
        return combined_data

    if st.button("🔊 Generate ElevenLabs Premium Story", type="primary"):
        if not api_key:
            st.error("⚠️ कृपया आधी API Key टाका!")
        elif not story_text.strip():
            st.warning("⚠️ कृपया कथा लिहा!")
        else:
            with st.spinner("✨ ElevenLabs HD आवाज जोडत आहे..."):
                full_audio = generate_eleven_story(story_text, api_key)
                if full_audio:
                    st.success("🎉 Premium HD Story तयार झाली!")
                    st.audio(bytes(full_audio), format="audio/mp3")
                    st.download_button("📥 MP3 Download करा", bytes(full_audio), file_name="alliwar_eleven_story.mp3", mime="audio/mp3")

# ==========================================
# 🆓 3. SINGLE VOICE FREE MODE
# ==========================================
elif "Single Voice Free" in engine_choice:
    st.success("✅ **Single Voice Free Mode:** १२ भारतीय भाषा + फॉरेन भाषा")

    lang_map = {
        "मराठी (Marathi)": {"Male": "mr-IN-MadhavNeural", "Female": "mr-IN-AarohiNeural"},
        "हिंदी (Hindi)": {"Male": "hi-IN-MadhurNeural", "Female": "hi-IN-SwaraNeural"},
        "English (India)": {"Male": "en-IN-PrabhatNeural", "Female": "en-IN-NeerjaNeural"},
        "தமிழ் (Tamil)": {"Male": "ta-IN-ValluvarNeural", "Female": "ta-IN-PallaviNeural"},
        "తెలుగు (Telugu)": {"Male": "te-IN-MohanNeural", "Female": "te-IN-ShrutiNeural"},
        "English (US)": {"Male": "en-US-GuyNeural", "Female": "en-US-AriaNeural"}
    }

    col_lang, col_gender = st.columns(2)
    with col_lang:
        selected_lang = st.selectbox("🌐 भाषा निवडा:", list(lang_map.keys()))
    with col_gender:
        selected_gender = st.selectbox("🎭 पात्र / लिंग:", ["Male (पुरुष)", "Female (स्त्री)"])

    gender_key = "Male" if "Male" in selected_gender else "Female"
    voice_code = lang_map[selected_lang][gender_key]

    col_speed, col_pitch = st.columns(2)
    with col_speed:
        speed_val = st.slider("⚡ Speed:", -50, 50, 0, 5, format="%d%%")
        speed_str = f"{speed_val:+d}%"
    with col_pitch:
        pitch_val = st.slider("🎵 Pitch:", -50, 50, 0, 5, format="%dHz")
        pitch_str = f"{pitch_val:+d}Hz"

    text_input = st.text_area("📝 मजकूर लिहा:", height=150)

    async def generate_edge_audio(text, voice, rate, pitch):
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            output_filename = tmp_file.name
        await communicate.save(output_filename)
        return output_filename

    if st.button("🔊 Generate Single Free Voice", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ कृपया मजकूर लिहा!")
        else:
            with st.spinner("✨ आवाज तयार होत आहे..."):
                try:
                    audio_path = asyncio.run(generate_edge_audio(text_input, voice_code, speed_str, pitch_str))
                    with open(audio_path, "rb") as f:
                        audio_data = f.read()
                        st.success("🎉 आवाज तयार झाला!")
                        st.audio(audio_data, format="audio/mp3")
                        st.download_button("📥 MP3 Download करा", audio_data, file_name="alliwar_single.mp3", mime="audio/mp3")
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ==========================================
# 💎 4. SINGLE VOICE PREMIUM MODE
# ==========================================
else:
    st.info("💎 **Single Voice Premium Mode:** ElevenLabs Voice Generator")
    api_key = st.text_input("🔑 ElevenLabs API Key:", type="password")
    
    eleven_voices = {
        "Adam (Deep Male)": "pNInz6obpgDQGcFmJgQb",
        "Rachel (Calm Female)": "21m00Tcm4TlvDq8ikWAM",
        "Domi (Energetic Female)": "AZnzlk1XvdvUeBnXmlld",
        "Bella (Soft Female)": "EXAVITQu4vr4xnSDxMaL"
    }

    selected_ev = st.selectbox("🎙️ पात्र निवडा:", list(eleven_voices.keys()))
    ev_id = eleven_voices[selected_ev]
    text_input = st.text_area("📝 मजकूर लिहा:", height=150)

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
