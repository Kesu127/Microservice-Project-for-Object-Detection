from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    # Send file to AI backend
    response = requests.post('http://localhost:8000/predict', files={'file': file})
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
