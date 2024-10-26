import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
import time
import os

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.mimetype.startswith('image/'):
        return jsonify({"error": "File is not an image"}), 400

    # Retry mechanism to connect to the backend
    max_retries = 5
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            response = requests.post('http://backend:8000/predict', files={'file': file})
            response.raise_for_status()
            data = response.json()
            image_base64 = data.get("image")
            prediction = data.get("predictions")
            return render_template('display.html', image_data=image_base64,prediction=prediction)
  
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return jsonify({"error": "Failed to connect to the backend"}), 500
        except requests.exceptions.HTTPError as http_err:
            return jsonify({"error": f"Backend returned an error: {http_err}"}), 500
        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/display/<path:filename>', methods=['GET'])
def display_image(filename):
    return render_template('display.html', filename=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
