import streamlit as st
from st_audiorec import st_audiorec

st.title("Pronounce-Analyzer")
st.write(
    "using Streamlit Audio Recorder."
)

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')