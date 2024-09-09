import streamlit as st
from st_audiorec import st_audiorec

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')

#st.title("🎈 My new app")
#st.write(
#    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#)
