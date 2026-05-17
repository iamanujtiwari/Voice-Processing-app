import streamlit as st
from audio_recorder_streamlit import audio_recorder
import soundfile as sf
import numpy as np
from scipy.signal import resample
from scipy.ndimage import gaussian_filter1d
import tempfile
import os

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Advanced AI Voice Changer",
    layout="centered"
)

st.title("🎤 Advanced AI Voice Changer")
st.write(" select a voice as per your choice and to record your voice click on the microphone icon and then click on the play button to listen to your changed voice and download it if you like it. ")
# ---------------- AUDIO RECORDER ---------------- #

audio_bytes = audio_recorder()

# ---------------- VOICE OPTIONS ---------------- #

option = st.selectbox(
    "Choose your voice style",
    (
        "Male 👨",
        "Female 👩",
        "Child 🧒",
        "Robot 🤖",
        "Alien 👽",
        "Radio 📻",
        "Deep Voice 🔥",
        "Echo 🌌"
    ),
)

# ---------------- MAIN PROCESSING ---------------- #

if audio_bytes:

    st.subheader("🎙 Original Voice")

    st.audio(audio_bytes, format="audio/wav")

    # Save temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        input_path = temp_audio.name

    # Load audio
    data, samplerate = sf.read(input_path)

    # Convert stereo to mono
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Convert to float32
    data = data.astype(np.float32)

    # Normalize input
    peak = np.max(np.abs(data))

    if peak > 0:
        data = data / peak

    # ---------------- VOICE EFFECTS ---------------- #

    # FEMALE VOICE
    if option == "Female 👩":

        # Slight pitch increase
        changed = resample(data, int(len(data) * 0.90))

        # Soft compression
        changed = np.tanh(changed * 1.6)

        # Time axis
        t = np.arange(len(changed)) / samplerate

        # Vocal shimmer
        shimmer1 = 0.015 * np.sin(2 * np.pi * 7 * t)
        shimmer2 = 0.008 * np.sin(2 * np.pi * 14 * t)

        changed = changed + shimmer1 + shimmer2

        # Light airy texture
        airy_noise = np.random.normal(0, 0.0012, len(changed))

        changed = changed + airy_noise

        # Soft echo
        delay = int(0.03 * samplerate)

        echo = np.zeros_like(changed)

        echo[delay:] = changed[:-delay]

        changed = changed + 0.12 * echo

        # Smooth harsh frequencies
        changed = gaussian_filter1d(changed, sigma=0.4)

        # Brightness boost
        changed = changed * 1.15

    # MALE VOICE
    elif option == "Male 👨":

        changed = resample(data, int(len(data) * 1.12))

        changed = np.tanh(changed * 1.7)

        changed = gaussian_filter1d(changed, sigma=0.5)

        changed = changed * 1.1

    # CHILD VOICE
    elif option == "Child 🧒":

        changed = resample(data, int(len(data) * 0.70))

        changed = np.tanh(changed * 1.5)

        changed = gaussian_filter1d(changed, sigma=0.3)

    # DEEP VOICE
    elif option == "Deep Voice 🔥":

        changed = resample(data, int(len(data) * 1.35))

        changed = np.tanh(changed * 2.0)

        changed = gaussian_filter1d(changed, sigma=0.6)

    # ROBOT VOICE
    elif option == "Robot 🤖":

        t = np.arange(len(data)) / samplerate

        mod1 = np.sin(2 * np.pi * 30 * t)
        mod2 = np.sin(2 * np.pi * 60 * t)
        mod3 = np.sin(2 * np.pi * 90 * t)

        robotic = data * (0.5 * mod1 + 0.3 * mod2 + 0.2 * mod3)

        robotic = np.tanh(robotic * 4)

        delay = int(0.04 * samplerate)

        echo = np.zeros_like(robotic)

        echo[delay:] = robotic[:-delay]

        changed = robotic + 0.5 * echo

    # ALIEN VOICE
    elif option == "Alien 👽":

        t = np.arange(len(data)) / samplerate

        alien_mod = np.sin(2 * np.pi * 120 * t)

        changed = data * alien_mod

        changed = np.tanh(changed * 5)

    # RADIO VOICE
    elif option == "Radio 📻":

        changed = np.tanh(data * 2.5)

        noise = np.random.normal(0, 0.015, len(changed))

        changed = changed + noise

        changed = gaussian_filter1d(changed, sigma=0.2)

    # ECHO VOICE
    elif option == "Echo 🌌":

        delay = int(0.2 * samplerate)

        echo = np.zeros_like(data)

        echo[delay:] = data[:-delay]

        changed = data + 0.6 * echo

    else:
        changed = data

    # ---------------- DSP RESET / FINAL MASTERING ---------------- #

    # Remove DC offset
    changed = changed - np.mean(changed)

    # Soft limiter
    changed = np.tanh(changed * 1.2)

    # Safe normalization
    peak = np.max(np.abs(changed))

    if peak > 0:
        changed = changed / peak

    # Final loudness
    changed = changed * 0.92

    # Prevent clipping
    changed = np.clip(changed, -1.0, 1.0)

    # Convert to float32
    changed = changed.astype(np.float32)

    # ---------------- SAVE OUTPUT ---------------- #

    output_path = "changed_voice.wav"

    sf.write(output_path, changed, samplerate)

    st.success("✅ Voice changed successfully!")

    # ---------------- PLAY OUTPUT ---------------- #

    st.subheader("🎧 Changed Voice")

    st.audio(output_path)

    # ---------------- DOWNLOAD BUTTON ---------------- #

    with open(output_path, "rb") as file:

        st.download_button(
            label="⬇ Download Changed Voice",
            data=file,
            file_name= option + " Voice.wav",
            mime="audio/wav"
        )

    # ---------------- CLEANUP ---------------- #

    os.remove(input_path)
    os.remove(output_path)