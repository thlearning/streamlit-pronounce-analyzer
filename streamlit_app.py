import streamlit as st
#from st_audiorec import st_audiorec
from audiorecorder import audiorecorder
import librosa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import streamlit.components.v1 as components
import ffmpeg

st.title("Pronounce-Analyzer")

#########################################
st.write(
    "Reference audio"
)
audio_file = open('believe.mp3', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/mpeg')

y, sr = librosa.load('believe.mp3', sr=16000)
fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios': [1, 2.5]})

# Draw waveform ################################
librosa.display.waveshow(y, sr=sr, ax=ax[0])

# Draw spectrogram ################################

#### melspectrogram #########
#S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=32, n_mels=256, fmax=8000)
#S_dB = librosa.power_to_db(S, ref=np.max)
#img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, ax=ax)

#### stft ####
hop_length = 32
D = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop_length))
D_db = librosa.amplitude_to_db(D, ref=np.max)
img = librosa.display.specshow(D_db, x_axis='time', y_axis='log', hop_length=hop_length, sr=sr, ax=ax[1])
##############

#ax[1].set(title='Spectrogram')
#fig.colorbar(img, ax=ax[1], format='%+2.0f dB')

st.pyplot(fig)
#########################################

# Animation #############################
# https://stackoverflow.com/questions/61808191/is-there-an-easy-way-to-animate-a-scrolling-vertical-line-in-matplotlib
duration = 0.54 # in sec
refreshPeriod = 20 # in ms

# fig2,ax2 = plt.subplots()
vl = ax[1].axvline(0, ls='-', color='w', lw=2, zorder=10)
ax[1].set_xlim(0,duration)

def animate(i,vl,period):
    t = i*period / 1000
    vl.set_xdata([t,t])
    return vl,

#animation = FuncAnimation(fig, animate, frames=int(duration/(refreshPeriod/1000)), fargs=(vl,refreshPeriod), interval=refreshPeriod)
#animation.save(filename='video.mp4', writer='ffmpeg')

#audio = ffmpeg.input('believe.mp3')
#video = ffmpeg.input('video.mp4')
#ffmpeg.concat(video, audio, v=1, a=1).output('outputvideo.mp4').run(overwrite_output=True)

#video_file = open('outputvideo.mp4', 'rb')
#video_bytes = video_file.read()

#st.video(video_bytes)

# Recording #############################
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

    y, sr = librosa.load('audio.wav', sr=16000)
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)

    # Draw waveform ################################
    librosa.display.waveshow(y, sr=sr, ax=ax[0])

    # Draw spectrogram #############################    
    hop_length = 32
    D = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop_length))
    D_db = librosa.amplitude_to_db(D, ref=np.max)
    
    img = librosa.display.specshow(D_db, x_axis='time', y_axis='log', hop_length=hop_length, sr=sr, ax=ax[1])
    #ax[1].set(title='Spectrogram')
    #fig.colorbar(img, ax=ax[1], format='%+2.0f dB')
    
    st.pyplot(fig)

