import os
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def create_waveform_visual(audio, sr, theme="abstract", output_path="assets/waveform.png"):
    """
    Creates a themed waveform visual from audio data and saves it to the specified location.

    Parameters:
        audio (numpy.ndarray): The audio signal array.
        sr (int): The sample rate of the audio signal.
        theme (str): The visual theme ('abstract', 'nature', 'retro').
        output_path (str): The file path where the waveform image will be saved.

    Raises:
        ValueError: If the audio is not a NumPy array or the sample rate is not a positive integer.
    """
    # Validate inputs
    if not isinstance(audio, np.ndarray):
        raise ValueError("Audio input must be a NumPy array.")
    if not isinstance(sr, int) or sr <= 0:
        raise ValueError("Sample rate (sr) must be a positive integer.")
    
    # Define color schemes based on theme
    color_schemes = {
        "abstract": ("#6a0dad", "#ffffff"),
        "nature": ("#228b22", "#d3f8e2"),
        "retro": ("#ff4500", "#ffe4b5")
    }
    line_color, bg_color = color_schemes.get(theme, ("#000000", "#ffffff"))

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate and save the waveform visual
    plt.figure(figsize=(10, 4), facecolor=bg_color)
    librosa.display.waveshow(audio, sr=sr, color=line_color)
    plt.title("Audio Waveform", color=line_color)
    plt.xlabel("Time (s)", color=line_color)
    plt.ylabel("Amplitude", color=line_color)
    plt.gca().set_facecolor(bg_color)
    plt.tight_layout()
    plt.savefig(output_path, transparent=True)
    plt.close()

    print(f"Waveform visual saved to {output_path}")
