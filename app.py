from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle music file upload
        music_file = request.files['music']
        if music_file and music_file.filename.endswith(('.mp3', '.wav')):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], music_file.filename)
            music_file.save(file_path)

            # Handle theme selection
            theme = request.form['theme']
            return f"File uploaded to {file_path} with theme {theme}!"
        else:
            return "Invalid file type. Please upload a .mp3 or .wav file."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
