from fastapi import FastAPI, File, UploadFile
import uvicorn
from model import detect_objects
from PIL import Image
import io

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    predictions, processed_image = detect_objects(image)
    
    # Save the processed image and JSON response
    processed_image.save(f"output/{file.filename}")
    with open(f"output/{file.filename.split('.')[0]}.json", "w") as f:
        f.write(predictions)
        
    return predictions

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
