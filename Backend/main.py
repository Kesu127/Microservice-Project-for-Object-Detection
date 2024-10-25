import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from model import detect_objects
from PIL import Image, UnidentifiedImageError
import io
import os

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

# Ensure the output directory exists
os.makedirs("output", exist_ok=True)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        logging.info("Received file: %s", file.filename)

        # Attempt to open the uploaded image file
        try:
            image = Image.open(io.BytesIO(await file.read()))
            logging.info("Image successfully opened")
        except UnidentifiedImageError:
            logging.error("Uploaded file is not a valid image")
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")

        # Perform object detection and get processed image with bounding boxes
        predictions, processed_image = detect_objects(image)
        logging.info("Object detection completed")

        # Set output file names
        image_filename = file.filename if file.filename else "output_image.png"
        image_path = f"output/{image_filename}"
        json_path = f"output/{image_filename.split('.')[0]}.json"

        # Save the processed image with bounding boxes
        processed_image.save(image_path, format="PNG")
        logging.info("Processed image saved as %s", image_path)

        # Save predictions as JSON
        with open(json_path, "w") as f:
            import json
            json.dump(predictions, f)
        logging.info("Predictions JSON saved as %s", json_path)

        return predictions

    except HTTPException as http_err:
        logging.error(f"HTTP error occurred: {http_err.detail}")
        raise http_err

    except Exception as e:
        logging.exception("An unexpected error occurred")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
