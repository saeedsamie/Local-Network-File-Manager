import os
import socket

import pyqrcode
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

PORT = 54321
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception as e:
        IP = '127.0.0.1'
        print(e)
    finally:
        s.close()
    return IP


def display_qr_code():
    ip_address = get_ip_address()
    data = f'http://{ip_address}:{PORT}'
    qr = pyqrcode.create(data)
    print("Scan this QR code with your device to connect:")
    print(qr.terminal(quiet_zone=1, background="black", module_color='white'))


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
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


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


display_qr_code()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=PORT)
