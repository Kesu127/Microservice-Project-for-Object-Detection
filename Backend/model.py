import torch
from PIL import Image, ImageDraw, ImageFont
import json

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_objects(image):
    results = model(image)
    predictions = results.pandas().xyxy[0].to_json(orient="records")
    try:
        font = ImageFont.truetype("arial.ttf", 60)  # You can adjust the font size as needed
    except IOError:
        font = ImageFont.load_default() 
    # Draw bounding boxes and labels on the image
    draw = ImageDraw.Draw(image)
    for _, row in results.pandas().xyxy[0].iterrows():
        draw.rectangle([row['xmin'], row['ymin'], row['xmax'], row['ymax']], outline="yellow", width=4)
        draw.text((row['xmin'], row['ymin']), row['name'], fill="black",font=font)
    
    return predictions, image
