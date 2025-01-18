from moviepy.audio.io.AudioFileClip import AudioFileClip  # For audio
from moviepy.video.VideoClip import ImageClip  # For video (image)
import numpy as np
from PIL import Image
import sys

def ignore_tkinter_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            if str(e).startswith("main thread is not in main loop"):
                pass
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
        
        # Resize the image to fit within the desired dimensions
        img.thumbnail((width, height))
        
        # Create an ImageClip from the resized image
        visual_clip = ImageClip(np.array(img)).set_duration(audio_clip.duration)
        
        # Position the visual clip at the center of the frame
        x_center = (width - img.width) // 2
        y_center = (height - img.height) // 2
        visual_clip = visual_clip.set_position((x_center, y_center))
        
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
        if 'visual_clip' in locals():
            visual_clip.close()
        if 'final_clip' in locals():
            final_clip.close()

# Example usage:
# generate_video("path/to/audio.mp3", "path/to/image.jpg", "output/video.mp4")

if __name__ == "__main__":
    # Your main execution logic here
    pass