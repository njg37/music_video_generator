from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for matplotlib
from utils.audio_analysis import analyze_audio
from utils.visual_effects import create_waveform_visual
from utils.video_generator import generate_video
from datetime import datetime

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'jpg', 'jpeg', 'png', 'gif'}

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
        audio_file = request.files.get('audio')
        image_file = request.files.get('image')  # Optional image upload

        # Validate audio file
        if audio_file and allowed_file(audio_file.filename):
            audio_filename = secure_filename(audio_file.filename)
            audio_filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            audio_file.save(audio_filepath)
            print(f"Audio file saved to: {audio_filepath}")

            try:
                # Analyze the audio file
                tempo, beats, waveform = analyze_audio(audio_filepath)
                sr = 22050  # Pass dynamically if `analyze_audio` provides it

                # Validate and handle image file
                if image_file and allowed_file(image_file.filename):
                    image_filename = secure_filename(image_file.filename)
                    visual_image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                    image_file.save(visual_image_path)
                    print(f"Uploaded image saved to: {visual_image_path}")
                else:
                    visual_image_path = os.path.join('assets', 'waveform.png')
                    create_waveform_visual(waveform, sr, output_path=visual_image_path)
                    print(f"Generated waveform image saved to: {visual_image_path}")

                # Generate video
                video_filename = f"music_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                video_output = os.path.join(app.config['OUTPUT_FOLDER'], video_filename)
                generate_video(audio_filepath, visual_image_path, video_output)
                print(f"Generated video saved to: {video_output}")

                if os.path.exists(video_output):
                    return f"Video generated successfully! You can download it from <a href='/download/{video_filename}'>here</a>."
                else:
                    return "Error: Video file not generated. Please check the logs."

            except Exception as e:
                print(f"Error during processing: {e}")
                return "An error occurred during video generation. Please try again."
        else:
            return "Invalid file type. Please upload a .mp3, .wav, .m4a, or a valid image file."

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
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable
    app.run(host="0.0.0.0", port=port, debug=False)
