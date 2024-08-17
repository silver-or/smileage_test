from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import base64
from io import BytesIO
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
import mediapipe as mp
import numpy as np
import os
import logging

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 모델 및 프로세서 로드
processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")
mp_selfie_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

# Pydantic 모델 정의
class ImageData(BaseModel):
    image: str = Field(..., description="Base64 encoded image")

# 유틸리티 함수들
def decode_image(image_data: str) -> Image.Image:
    try:
        image_bytes = base64.b64decode(image_data.split(',')[1])
        return Image.open(BytesIO(image_bytes))
    except Exception as e:
        logger.error("Failed to decode image: %s", e)
        raise ValueError("Invalid image data") from e

def preprocess_image(image: Image.Image) -> dict:
    return processor(images=image, return_tensors="pt")

def infer_image(inputs: dict) -> tuple[torch.Tensor, torch.Tensor]:
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    return logits, probabilities

def postprocess_results(logits: torch.Tensor, probabilities: torch.Tensor) -> list:
    results = [
        (model.config.id2label[i], round(prob.item() * 100, 2))
        for i, prob in enumerate(probabilities[0])
    ]
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:3]

def remove_background_mediapipe(image: Image.Image) -> Image.Image:
    image_np = np.array(image)
    results = mp_selfie_segmentation.process(image_np)
    mask = results.segmentation_mask > 0.5

    alpha_channel = (mask * 255).astype(np.uint8)
    image_rgba = np.dstack((image_np, alpha_channel))

    return Image.fromarray(image_rgba, 'RGBA')

def set_background(image: Image.Image, background_path: str) -> Image.Image:
    try:
        background = Image.open(background_path).convert("RGBA")
        background = background.resize(image.size)
        combined = Image.alpha_composite(background, image)
        return combined
    except Exception as e:
        logger.error("Failed to set background: %s", e)
        raise ValueError("Failed to set background image") from e

def encode_image(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

@app.post("/infer/")
async def infer(data: ImageData):
    try:
        image = decode_image(data.image)
        processed_image = remove_background_mediapipe(image)

        inputs = preprocess_image(image)
        logits, probabilities = infer_image(inputs)

        results = postprocess_results(logits, probabilities)

        if results:
            emotion = results[0][0]
            background_path = os.path.join("src", f"{emotion}.jpg") if emotion in ["happy", "sad", "angry"] else None
            if background_path and os.path.exists(background_path):
                processed_image = set_background(processed_image, background_path)

        encoded_image = encode_image(processed_image)

        return {"results": results, "processed_image": encoded_image}
    except ValueError as ve:
        logger.error("ValueError: %s", ve)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
