import librosa
import numpy as np

def analyze_audio(file_path):
    # Load the audio file
    audio, sr = librosa.load(file_path)

    # Extract tempo and beat frames
    tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)

    # Compute waveform (amplitude values over time)
    waveform = audio[:min(len(audio), sr * 30)]  # Extract the first 30 seconds for simplicity
    return tempo, beats, waveform
