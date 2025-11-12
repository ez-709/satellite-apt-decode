from flask import Flask, request
import os
from datetime import datetime
import argparse

def create_vm_server(upload_dir, port=5000):
    os.makedirs(upload_dir, exist_ok=True)

    app = Flask(__name__)
    UPLOAD_DIR = upload_dir

    @app.route('/upload_wav', methods=['POST'])
    def receive_wav():
        if 'file' not in request.files:
            return "No file", 400
        file = request.files['file']
        if file.filename == '':
            return "Empty filename", 400
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wav_{timestamp}.wav"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        file.save(file_path)
        print(f"Saved file: {file_path}")  # For debugging
        return "OK", 20
    
    print(f"Server starting on port {port}, saving to: {UPLOAD_DIR}")
    app.run(host='0.0.0.0', port=port)


parser = argparse.ArgumentParser(description='VM HTTP Server for receiving .wav files')
parser.add_argument('D:', required=True, help='Directory to save received files')
parser.add_argument('--port', type=int, default=5000, help='Port to run server on (default: 5000)')

args = parser.parse_args()

create_vm_server(upload_dir=args.upload_dir, port=args.port)