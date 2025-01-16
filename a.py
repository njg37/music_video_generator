import librosa
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# Import resize and speedx (use existing fx modules)
try:
    from moviepy.video.fx.resize import resize
    from moviepy.video.fx.speedx import speedx
except ImportError:
    resize = None
    speedx = None
    print("Resize or speedx functions are unavailable in the current moviepy version.")

print("Setup successful!")
