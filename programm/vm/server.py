from flask import Flask, request

class VM_server:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/ping', methods=['GET'])
        def ping():
            return "pong", 200

        @self.app.route('/receive_file', methods=['POST'])
        def receive_file():
            if 'file' not in request.files:
                return "No file", 400
            
            file = request.files['file']
            if file.filename == '':
                return "Empty filename", 400
            
            file.save(file.filename)
            print(f"Получен файл: {file.filename}")
            return "File received", 200

    def run(self):
        print(f"Сервер запущен на {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=False)