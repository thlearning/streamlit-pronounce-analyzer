import streamlit as st
from st_audiorec import st_audiorec
from audiorecorder import audiorecorder
import librosa

st.title("Pronounce-Analyzer")
st.write(
    "using Streamlit Audio Recorder. https://github.com/stefanrmmr/streamlit-audio-recorder"
)

#########################################

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')

#########################################

st.write(
    "using streamlit-audiorecorder. https://github.com/theevann/streamlit-audiorecorder"
)

audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.export().read())  

    # To save audio to a file, use pydub export method:
    audio.export("audio.wav", format="wav")

    # To get audio properties, use pydub AudioSegment properties:
    st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

#########################################
y, sr = librosa.load(librosa.ex('/sound/believe.mp3'))