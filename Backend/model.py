import torch
from PIL import Image, ImageDraw
import json

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_objects(image):
    results = model(image)
    predictions = results.pandas().xyxy[0].to_json(orient="records")
    
    # Draw bounding boxes on the image
    draw = ImageDraw.Draw(image)
    for _, row in results.pandas().xyxy[0].iterrows():
        draw.rectangle([row['xmin'], row['ymin'], row['xmax'], row['ymax']], outline="red", width=2)
    
    return predictions, image
