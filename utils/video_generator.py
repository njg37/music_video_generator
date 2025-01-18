from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
import numpy as np
from PIL import Image

def ignore_tkinter_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            if str(e).startswith("main thread is not in main loop"):
                print("Ignored a tkinter-related RuntimeError.")
            else:
                raise
    return wrapper

@ignore_tkinter_exceptions
def generate_video(audio_file, visual_file, output_file):
    try:
        # Load the audio
        audio_clip = AudioFileClip(audio_file)
        
        # Load the visual (image)
        img = Image.open(visual_file)
        width, height = 1920, 1080  # Desired dimensions
        
        # Resize the image
        img.thumbnail((width, height))
        
        # Create an ImageClip
        visual_clip = ImageClip(np.array(img)).set_duration(audio_clip.duration)
        
        # Combine the audio and visual clips
        final_clip = visual_clip.set_audio(audio_clip)
        
        # Write the video to file
        final_clip.write_videofile(
            output_file,
            codec="libx264",
            audio_codec="aac",
            fps=24
        )
        print(f"Video successfully generated: {output_file}")
        
    except Exception as e:
        print(f"Error generating video: {e}")
        
    finally:
        # Ensure resources are released
        if 'audio_clip' in locals():
            audio_clip.close()
        if 'final_clip' in locals():
            final_clip.close()
        if 'img' in locals():
            img.close()  # Close the image to release resources
