from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import uuid
import sys

# Add parent directory to path to import zero_stego
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zero_stego import process_sender, process_receiver, load_image, calculate_psnr

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Use /tmp for serverless environment
UPLOAD_FOLDER = '/tmp/uploads'
KEYS_FOLDER = '/tmp/keys'
RECOVERED_FOLDER = '/tmp/recovered'

for folder in [UPLOAD_FOLDER, KEYS_FOLDER, RECOVERED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sender', methods=['GET', 'POST'])
def sender():
    if request.method == 'POST':
        if 'cover' not in request.files or 'secret' not in request.files:
            return render_template('sender.html', error='Please upload both cover and secret images')
        
        cover_file = request.files['cover']
        secret_file = request.files['secret']
        
        if cover_file.filename == '' or secret_file.filename == '':
            return render_template('sender.html', error='Please select both files')
        
        if not (allowed_file(cover_file.filename) and allowed_file(secret_file.filename)):
            return render_template('sender.html', error='Invalid file type. Use PNG, JPG, BMP, or TIFF')
        
        session_id = str(uuid.uuid4())[:8]
        
        cover_path = os.path.join(UPLOAD_FOLDER, f'{session_id}_cover.png')
        secret_path = os.path.join(UPLOAD_FOLDER, f'{session_id}_secret.png')
        key_path = os.path.join(KEYS_FOLDER, f'{session_id}_stego_key.npy')
        
        cover_file.save(cover_path)
        secret_file.save(secret_path)
        
        try:
            shape = process_sender(cover_path, secret_path, key_path)
            return render_template('sender.html', 
                                   success=True,
                                   session_id=session_id,
                                   key_path=key_path,
                                   cover_path=cover_path,
                                   shape=f"{shape[0]}x{shape[1]}")
        except Exception as e:
            return render_template('sender.html', error=str(e))
    
    return render_template('sender.html')

@app.route('/receiver', methods=['GET', 'POST'])
def receiver():
    if request.method == 'POST':
        if 'cover' not in request.files or 'key' not in request.files:
            return render_template('receiver.html', error='Please upload both cover image and stego-key')
        
        cover_file = request.files['cover']
        key_file = request.files['key']
        
        if cover_file.filename == '' or key_file.filename == '':
            return render_template('receiver.html', error='Please select both files')
        
        if not allowed_file(cover_file.filename):
            return render_template('receiver.html', error='Invalid image file type')
        
        if not key_file.filename.endswith('.npy'):
            return render_template('receiver.html', error='Stego-key must be a .npy file')
        
        session_id = str(uuid.uuid4())[:8]
        
        cover_path = os.path.join(UPLOAD_FOLDER, f'{session_id}_cover.png')
        key_path = os.path.join(KEYS_FOLDER, f'{session_id}_key.npy')
        recovered_path = os.path.join(RECOVERED_FOLDER, f'{session_id}_recovered.png')
        
        cover_file.save(cover_path)
        key_file.save(key_path)
        
        try:
            recovered = process_receiver(cover_path, key_path, recovered_path)
            return render_template('receiver.html',
                                   success=True,
                                   session_id=session_id,
                                   recovered_path=recovered_path)
        except Exception as e:
            return render_template('receiver.html', error=str(e))
    
    return render_template('receiver.html')

ALLOWED_DOWNLOAD_DIRS = [KEYS_FOLDER, RECOVERED_FOLDER]

@app.route('/download/<path:filepath>')
def download_file(filepath):
    abs_path = os.path.abspath(filepath)
    allowed = False
    for allowed_dir in ALLOWED_DOWNLOAD_DIRS:
        abs_allowed = os.path.abspath(allowed_dir)
        if abs_path.startswith(abs_allowed + os.sep) or abs_path == abs_allowed:
            if os.path.isfile(abs_path):
                allowed = True
                break
    
    if not allowed:
        return "Access denied", 403
    
    return send_file(abs_path, as_attachment=True)

# Vercel serverless function handler
def handler(request, context=None):
    return app(request, context)

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
