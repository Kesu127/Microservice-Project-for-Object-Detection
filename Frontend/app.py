import requests
from flask import Flask, render_template, request

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
    
    # Update the API URL to 'http://backend:8000/predict'
    response = requests.post('http://backend:8000/predict', files={'file': file})
    
    # Return the JSON response from the backend
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Ensure Flask listens on all interfaces
