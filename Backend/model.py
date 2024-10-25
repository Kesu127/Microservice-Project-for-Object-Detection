import torch
from PIL import Image, ImageDraw

def detect_objects(image):
    # Load the YOLO model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.conf = 0.5  # Set confidence threshold

    # Run inference
    results = model(image)

    # Convert the predictions to a JSON-serializable format
    predictions = results.pandas().xyxy[0].to_dict(orient="records")

    # Draw bounding boxes on the image
    draw = ImageDraw.Draw(image)
    for pred in predictions:
        x_min, y_min, x_max, y_max = pred['xmin'], pred['ymin'], pred['xmax'], pred['ymax']
        draw.rectangle(((x_min, y_min), (x_max, y_max)), outline="red", width=3)
        draw.text((x_min, y_min), pred['name'], fill="red")

    return predictions, image  # Return both predictions and the image with bounding boxes
