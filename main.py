import numpy as np
import cv2
import secrets

from time import time
from loguru import logger
from typing import Annotated
from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from services.grounding_dino import ObjectDetectionServices
from model.object_detection_view_model import ObjectDetectionViewModel

class ResponseModel(BaseModel):
    response_data: list

model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    model["detector"] = ObjectDetectionServices("cpu") 
    yield
    model.clear()

app = FastAPI(lifespan=lifespan)
security = HTTPBasic()

@app.post("/ObjectDetection/detectObject", response_model=list[ObjectDetectionViewModel])
async def detectObject(prompt: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)], data: UploadFile = File(...)): 
    # if not (secrets.compare_digest(credentials.username.encode("utf8"), b"duongng2911") and secrets.compare_digest(credentials.password.encode("utf8"), b"hehehihi0808")):
    #     logger.error("Incorrect email or password")
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZEDm,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Basic"}
    #     )

    start_time = time()
    try:
        image_bytes = await data.read()
        
        # Convert bytes data to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decode the image using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = model["detector"].predict(image, prompt)
        logger.info(f"{result}")
        logger.info(f"Finished generate response: {time() - start_time:.2f} seconds")
        return result
    except Exception as error:
        logger.error(f"{error}")
        return {"result" : error}

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=3000, reload=True)