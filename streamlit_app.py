import streamlit as st
#from st_audiorec import st_audiorec
from audiorecorder import audiorecorder
import librosa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import streamlit.components.v1 as components

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
    y, sr = librosa.load('audio.wav', sr=16000)
    hop_length = 32
    D = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop_length))
    D_db = librosa.amplitude_to_db(D, ref=np.max)

    fig, ax = plt.subplots()
    img = librosa.display.specshow(D_db, x_axis='time', y_axis='log', hop_length=hop_length, sr=sr, ax=ax)
    ax.set(title='Spectrogram')
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    
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
#S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=32, n_mels=256, fmax=8000)
#S_dB = librosa.power_to_db(S, ref=np.max)
#img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, ax=ax)

#### stft ####
hop_length = 32
D = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop_length))
D_db = librosa.amplitude_to_db(D, ref=np.max)
img = librosa.display.specshow(D_db, x_axis='time', y_axis='log', hop_length=hop_length, sr=sr, ax=ax)
#############

ax.set(title='Spectrogram')
fig.colorbar(img, ax=ax, format='%+2.0f dB')

st.pyplot(fig)
#########################################

# Animation #############################
#fig2, ax2 = plt.subplots()
#line = plt.plot([], [], lw=2)

#def update_frame(t, line):
#    t = np.arange(0,t,0.1)
#    y = np.sin(t)
#    line.set_data(t, y)
#    return line

#animation = FuncAnimation(
#        fig2, update_frame, frames=np.arange(1,10,1), fargs=(line), interval=100, blit=False
#)

#with st.spinner("Preparing animation..."):
#        components.html(animation.to_jshtml(), height=1000)

# Animation2 #############################
# https://stackoverflow.com/questions/61808191/is-there-an-easy-way-to-animate-a-scrolling-vertical-line-in-matplotlib
duration = 0.54 # in sec
refreshPeriod = 100 # in ms

# fig2,ax2 = plt.subplots()
vl = ax.axvline(0, ls='-', color='r', lw=1, zorder=10)
ax.set_xlim(0,duration)

def animate(i,vl,period):
    t = i*period / 1000
    vl.set_xdata([t,t])
    return vl,

animation = FuncAnimation(fig, animate, frames=int(duration/(refreshPeriod/1000)), fargs=(vl,refreshPeriod), interval=refreshPeriod)
animation.save(filename='video.mp4', writer='ffmpeg')

video_file = open('video.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)