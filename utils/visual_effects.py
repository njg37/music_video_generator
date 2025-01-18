import os
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def create_waveform_visual(audio, sr, output_path="assets/waveform.png"):
    """
    Creates a waveform visual from audio data and saves it to the specified location.

    Parameters:
        audio (numpy.ndarray): The audio signal array.
        sr (int): The sample rate of the audio signal.
        output_path (str): The file path where the waveform image will be saved.

    Raises:
        ValueError: If the audio is not a NumPy array or the sample rate is not a positive integer.
    """
    # Validate inputs
    if not isinstance(audio, np.ndarray):
        raise ValueError("Audio input must be a NumPy array.")
    if not isinstance(sr, int) or sr <= 0:
        raise ValueError("Sample rate (sr) must be a positive integer.")
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate and save the waveform visual
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(audio, sr=sr)
    plt.title("Audio Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(output_path)  # Save to the specified output path
    plt.close()

    print(f"Waveform visual saved to {output_path}")
