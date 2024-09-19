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
fig2, ax2 = plt.subplots()
t = np.linspace(0, 3, 40)
g = -9.81
v0 = 12
z = g * t**2 / 2 + v0 * t

v02 = 5
z2 = g * t**2 / 2 + v02 * t

scat = ax2.scatter(t[0], z[0], c="b", s=5, label=f'v0 = {v0} m/s')
line2 = ax2.plot(t[0], z2[0], label=f'v0 = {v02} m/s')[0]
ax2.set(xlim=[0, 3], ylim=[-4, 10], xlabel='Time [s]', ylabel='Z [m]')
ax2.legend()


def update(frame):
    # for each frame, update the data stored on each artist.
    x = t[:frame]
    y = z[:frame]
    # update the scatter plot:
    data = np.stack([x, y]).T
    scat.set_offsets(data)
    # update the line plot:
    line2.set_xdata(t[:frame])
    line2.set_ydata(z2[:frame])
    return (scat, line2)


animation = FuncAnimation(fig=fig2, func=update, frames=40, interval=30)

with st.spinner("Preparing animation..."):
        components.html(animation.to_jshtml(), height=1000)