import streamlit as st
#from st_audiorec import st_audiorec
from audiorecorder import audiorecorder
import librosa
import matplotlib.pyplot as plt
import numpy as np

st.title("Pronounce-Analyzer")

#########################################
#st.write(
#    "using Streamlit Audio Recorder. https://github.com/stefanrmmr/streamlit-audio-recorder"
#)
#wav_audio_data = st_audiorec()
#
#if wav_audio_data is not None:
#    st.audio(wav_audio_data, format='audio/wav')
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

    # Draw spectrogram! ################################
    y, sr = librosa.load('audio.wav', sr=32000)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=6000)

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
    "Reference audio"
)
audio_file = open('believe.mp3', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/mpeg')

# Draw spectrogram! ################################
y, sr = librosa.load('believe.mp3', sr=16000)

fig, ax = plt.subplots()

#### melspectrogram #########
S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=32, n_mels=256, fmax=8000)
S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, ax=ax)

#### stft ####
hop_length = 32
D = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop_length))
D_db = librosa.amplitude_to_db(D, ref=np.max)
#img = librosa.display.specshow(D_db, x_axis='time', y_axis='log', sr=sr, ax=ax)
#############

fig.colorbar(img, ax=ax, format='%+2.0f dB')
ax.set(title='Mel-frequency spectrogram')
st.pyplot(fig)
#########################################

