from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from utils.audio_analysis import analyze_audio
from utils.visual_effects import create_waveform_visual
from utils.video_generator import generate_video

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create folders if they do not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle music file upload
        file = request.files.get('audio')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                # Analyze the audio file (tempo, beats, waveform)
                tempo, beats, waveform = analyze_audio(filepath)

                # Create visual based on the audio
                visual_image_path = os.path.join('assets', 'waveform.png')
                os.makedirs('assets', exist_ok=True)  # Ensure assets directory exists
                create_waveform_visual(waveform, 22050)

                # Generate video with audio and visual
                video_filename = 'music_video.mp4'
                video_output = os.path.join(app.config['OUTPUT_FOLDER'], video_filename)
                generate_video(filepath, visual_image_path, video_output)

                # Debugging: Check paths
                print("Output folder absolute path:", os.path.abspath(app.config['OUTPUT_FOLDER']))
                print("Generated video file path:", video_output)

                # Ensure the file exists before returning the download link
                if os.path.exists(video_output):
                    return f"Video generated successfully! You can download it from <a href='/download/{video_filename}'>here</a>."
                else:
                    return "Error: Video file not generated. Please check the logs."

            except Exception as e:
                # Handle any exceptions and log errors
                print(f"Error during processing: {e}")
                return "An error occurred during video generation. Please try again."

        else:
            return "Invalid file type. Please upload a .mp3, .wav, or .m4a file."
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        print(f"Trying to serve file: {file_path}")
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        print(f"Error serving file: {e}")
        return f"Error: Unable to serve the file '{filename}'."

if __name__ == '__main__':
    app.run(debug=True)
