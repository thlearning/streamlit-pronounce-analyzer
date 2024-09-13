import streamlit as st
from st_audiorec import st_audiorec
from audiorecorder import audiorecorder
import librosa
import matplotlib.pyplot as plt
import numpy as np

st.title("Pronounce-Analyzer")
st.write(
    "using Streamlit Audio Recorder. https://github.com/stefanrmmr/streamlit-audio-recorder"
)

#########################################

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')
    y, sr = librosa.load('believe.mp3', sr=16000)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

    fig, ax = plt.subplots()
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time',
                             y_axis='mel', sr=sr,
                             fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')
    st.pyplot(fig)

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
st.write(
    "Audio"
)
audio_file = open('believe.mp3', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/mpeg')
#########################################

