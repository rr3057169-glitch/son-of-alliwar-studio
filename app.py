import streamlit as st
from gtts import gTTS
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
# 🎭 1. FREE MULTI-CHARACTER STORY MODE (Google Engine)
# ==========================================
if "Free Multi-Character" in engine_choice:
    st.success("✨ **Free Multi-Character Mode:** (100% Guaranteed Working)")
    
    lang_choice = st.selectbox("🌐 कथा भाषा (Language):", ["Marathi", "Hindi", "English"])
    
    lang_code_map = {
        "Marathi": "mr",
        "Hindi": "hi",
        "English": "en"
    }
    
    selected_lang_code = lang_code_map[lang_choice]

    st.markdown("""
    💡 **फॉर्मॅट:**  
    `राजू: अरे तू कुठे चाललास?`  
    `सीमा: मी बाजारात चालले आहे.`
    """)

    story_text = st.text_area("📝 कथा / संवाद लिहा:", height=200, placeholder="राजू: अरे सीमा तू कुठे चाललीस?\nसीमा: मी बाजारात चालले आहे, तू पण येतोस का?")

    if st.button("🔊 Generate Free Story Audio", type="primary"):
        if not story_text.strip():
            st.warning("⚠️ कृपया कथा लिहा!")
        else:
            with st.spinner("✨ आवाज तयार होत आहे..."):
                try:
                    lines = story_text.strip().split("\n")
                    combined_data = bytearray()
                    
                    for line in lines:
                        if not line.strip():
                            continue
                        
                        speaker_text = line.strip()

                        if ":" in line:
                            parts = line.split(":", 1)
                            speaker_text = parts[1].strip()

                        if speaker_text:
                            # Direct Google TTS - Zero Async Errors
                            tts = gTTS(text=speaker_text, lang=selected_lang_code, slow=False)
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                                tmp_name = tmp_file.name
                            
                            tts.save(tmp_name)
                            
                            with open(tmp_name, "rb") as f:
                                combined_data.extend(f.read())
                            if os.path.exists(tmp_name):
                                os.remove(tmp_name)

                    if combined_data:
                        st.success("🎉 Audio यशस्विरित्या तयार झाला!")
                        st.audio(bytes(combined_data), format="audio/mp3")
                        st.download_button("📥 MP3 Download करा", bytes(combined_data), file_name="alliwar_story.mp3", mime="audio/mp3")
                    else:
                        st.error("काहीतरी गडबड झाली, पुन्हा प्रयत्न करा.")

                except Exception as e:
                    st.error(f"Error details: {str(e)}")

# ==========================================
# 💎 2. PREMIUM MULTI-CHARACTER (ELEVENLABS)
# ==========================================
elif "Premium Multi-Character" in engine_choice:
    st.info("💎 **ElevenLabs Multi-Character Story Mode:** HD आवाज जनरेटर")
    
    api_key = st.text_input("🔑 ElevenLabs API Key टाका:", type="password")

    story_text = st.text_area("📝 कथा / संवाद लिहा:", height=200, placeholder="राजू: अरे सीमा तू कुठे चाललीस?\nसीमा: मी बाजारात चालले आहे.")

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

                if any(k in speaker_name for k in ["female", "girl", "woman", "स्त्री", "मुलगी", "सीमा", "पूजा", "राधा"]):
                    current_voice_id = eleven_female_id

            if speaker_text:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{current_voice_id}"
                headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": key}
                data = {"text": speaker_text, "model_id": "eleven_multilingual_v2"}
                
                res = requests.post(url, json=data, headers=headers)
                if res.status_code == 200:
                    combined_data.extend(res.content)
                else:
                    st.error(f"Error: {res.text}")
                    return None
        return combined_data

    if st.button("🔊 Generate ElevenLabs Premium Story", type="primary"):
        if not api_key:
            st.error("⚠️ कृपया API Key टाका!")
        elif not story_text.strip():
            st.warning("⚠️ कृपया कथा लिहा!")
        else:
            with st.spinner("✨ ElevenLabs HD आवाज तयार होत आहे..."):
                full_audio = generate_eleven_story(story_text, api_key)
                if full_audio:
                    st.success("🎉 Premium HD Story तयार झाली!")
                    st.audio(bytes(full_audio), format="audio/mp3")
                    st.download_button("📥 MP3 Download करा", bytes(full_audio), file_name="alliwar_eleven.mp3", mime="audio/mp3")

# ==========================================
# 🆓 3. SINGLE VOICE FREE MODE
# ==========================================
elif "Single Voice Free" in engine_choice:
    st.success("✅ **Single Voice Free Mode**")

    lang_map = {
        "मराठी (Marathi)": "mr",
        "हिंदी (Hindi)": "hi",
        "English": "en"
    }

    selected_lang = st.selectbox("🌐 भाषा निवडा:", list(lang_map.keys()))
    text_input = st.text_area("📝 मजकूर लिहा:", height=150)

    if st.button("🔊 Generate Single Free Voice", type="primary"):
        if not text_input.strip():
            st.warning("⚠️ कृपया मजकूर लिहा!")
        else:
            with st.spinner("✨ आवाज तयार होत आहे..."):
                try:
                    tts = gTTS(text=text_input, lang=lang_map[selected_lang], slow=False)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                        audio_path = tmp_file.name
                    tts.save(audio_path)

                    with open(audio_path, "rb") as f:
                        audio_data = f.read()
                        st.success("🎉 आवाज तयार झाला!")
                        st.audio(audio_data, format="audio/mp3")
                        st.download_button("📥 MP3 Download करा", audio_data, file_name="alliwar_single.mp3", mime="audio/mp3")
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                except Exception as e:
                    st.error(f"Error details: {str(e)}")

# ==========================================
# 💎 4. SINGLE VOICE PREMIUM MODE
# ==========================================
else:
    st.info("💎 **Single Voice Premium Mode:** ElevenLabs Generator")
    api_key = st.text_input("🔑 ElevenLabs API Key:", type="password")
    
    eleven_voices = {
        "Adam (Deep Male)": "pNInz6obpgDQGcFmJgQb",
        "Rachel (Calm Female)": "21m00Tcm4TlvDq8ikWAM"
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
