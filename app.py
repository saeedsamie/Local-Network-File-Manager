import os

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET'])
def index():
    # List files in the upload directory
    files_info = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        size = os.path.getsize(filepath)
        # Convert size from bytes to a more readable format
        size_kb = size / 1024  # Size in kilobytes
        size_mb = size_kb / 1024  # Size in megabytes
        files_info.append({
            'name': filename,
            'size_kb': round(size_kb, 2),
            'size_mb': round(size_mb, 2)
        })
    return render_template('index.html', files=files_info)


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist('files')
    for file in uploaded_files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return redirect(url_for('index'))
    except Exception as ee:
        print(ee)


@app.route('/ping')
def ping():
    return "Pong"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
