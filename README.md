# Microservice Project for Object Detection

This project implements a microservice architecture for performing object detection on images. It consists of a **Backend** service using FastAPI to handle image processing and object detection, and a **Frontend** service using Flask for uploading and displaying images with detected objects. The entire setup is containerized using Docker and managed with `docker-compose` for easy deployment.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Solution Approach](#solution-approach)
- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [References](#references)

## Overview

The system allows users to upload an image through a web interface, which then sends the image to the backend service for object detection. The backend processes the image, draws bounding boxes around detected objects, and returns the processed image and prediction data to the frontend. The frontend then displays the annotated image and JSON prediction data.

## Project Structure
```
Microservice Project for Object Detection
├── Backend
│   ├── Dockerfile           # Backend Docker configuration
│   ├── main.py              # FastAPI app with prediction endpoint
│   ├── model.py             # Object detection model and image processing
│   └── requirements.txt     # Backend dependencies
│
├── Frontend
│   ├── Dockerfile           # Frontend Docker configuration
│   ├── app.py               # Flask app for file upload and result display
│   ├── requirements.txt     # Frontend dependencies
│   ├── static
│   │   └── style.css        # CSS for frontend styling
│   └── templates
│       ├── display.html     # Display page for showing results
│       └── index.html       # Homepage with file upload form
│
├── docker-compose.yml       # Docker-compose setup for frontend and backend services
```
## Solution Approach

1. **Backend (Object Detection) Setup**:
   - The backend service leverages FastAPI for the REST API, where the `predict` endpoint receives an image file and performs object detection using a pre-trained **`YOLOv5`** model.
   - The `model.py` file handles model loading, object detection, and drawing bounding boxes on detected objects.
   - `main.py` orchestrates the API functionality, including error handling for non-image inputs and converting processed images to Base64 for easier transmission to the frontend.

2. **Frontend (User Interface) Setup**:
   - The frontend uses Flask to provide an interface where users can upload an image, which is then sent to the backend.
   - The `app.py` file handles the file upload, sends it to the backend’s `predict` endpoint, and retrieves the annotated image and predictions.
   - Uploaded files are saved in a temporary folder, and the frontend incorporates retry mechanisms to handle any backend connectivity issues.

3. **Dockerization**:
   - Docker images for both frontend and backend are defined with separate Dockerfiles, installing necessary dependencies and setting up working directories.
   - `docker-compose.yml` is configured to run both services, ensuring the frontend starts after the backend. The setup allows for scaling and restarting of services in case of failures.

### Steps to Reach the Solution

- **Choosing the Tech Stack**: Selected FastAPI for efficient backend API management, and Flask for a lightweight frontend, ensuring both could easily interact within Dockerized containers.
- **Model Selection**: YOLOv5 was chosen for object detection due to its high accuracy and efficiency.
- **Designing the System Flow**: Frontend-to-backend communication was structured to handle network latency and errors, with retry mechanisms in the frontend.
- **Docker and Deployment**: Dockerization of each service allowed for easy scalability and deployment, managed through `docker-compose`.

## Installation

1. **Clone the Repository**: 
    ```
    git clone https://github.com/Kesu127/microservice-object-detection.git
    cd microservice-object-detection
    ```

2. **Build and Run with Docker Compose**:
   ```
   docker-compose up --build
   ```

3. **Access the Application**:
   - Frontend: [http://localhost:5000](http://localhost:5000)
   - Backend: [http://localhost:8000/docs](http://localhost:8000/docs) (FastAPI docs)

4. **To Run on local**:
   - Frontend
     ```
     cd Frontend
     python app.py
     http://localhost:5000 // link to access Frontend 
     ```
   - Backend: 
      ```
      cd Backend
      uvicorn main:app --reload
      http://127.0.0.1:8000/docs  //link to access backend
      ```
## Usage

1. **Upload an Image**:
   - Open the frontend URL and upload an image.
   - The frontend sends the image to the backend for processing.

2. **View Results**:
   - The frontend will display:
     - The processed image with bounding boxes around detected objects.
     - JSON-formatted predictions showing details for each detected object.

## Output

After uploading an image, the output includes:

1. **Annotated Image**: Displayed in the frontend with bounding boxes around detected objects.
2. **JSON File**: A JSON object containing details of detected objects (e.g., label, confidence score, bounding box coordinates) is generated by the backend and displayed in the frontend.

UI
!["UI"](/Backend/output/Frontend%20UI.png)

UI OUTPUT
!["UI Output"](/Backend/output/Image%20Upload.png)
Example JSON output:
````
[
  {
    \"name\": \"object_label\",
    \"confidence\": 0.85,
    \"xmin\": 34,
    \"ymin\": 45,
    \"xmax\": 120,
    \"ymax\": 160
  },
  ...
]
````
PREDICTION 1
!["Prediction1"](/Backend/output/Prediction%201.png)

PREDICTION 2
!["Prediction2"](/Backend/output/Prediction%202.png)

PREDICTION 3
!["Prediction3"](/Backend/output/Prediction%203.png)
## References

- **YOLOv5 Model**: Utilized the official [Ultralytics YOLOv5 repository](https://github.com/ultralytics/yolov5) for object detection.
- **FastAPI Documentation**: [FastAPI](https://fastapi.tiangolo.com/) was referenced for building a scalable backend API.
- **Flask Documentation**: [Flask](https://flask.palletsprojects.com/) was used as a lightweight frontend framework for handling image uploads and rendering results.

