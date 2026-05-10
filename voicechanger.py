import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.title("Audio Recorder")

audio_bytes = audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    with open("recorded_audio.wav", "wb") as f:
        f.write(audio_bytes)

    st.success("Audio saved!")

option = st.selectbox(
    "chocie your voice style",
    ("Male", "Female", "chlidern","robotic voice"),
)

st.write("You selected:", option)