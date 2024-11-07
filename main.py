import numpy as np
import cv2
# import secrets

from time import time
from loguru import logger
# from typing import Annotated
from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Depends, status, HTTPException
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
from services.grounding_dino import ObjectDetectionServices
from model.object_detection_view_model import ObjectDetectionViewModel
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider
from prometheus_client import start_http_server

class ResponseModel(BaseModel):
    response_data: list

model = {}

# Traces using jeager
trace_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "serving-grounding-dino"}))
set_tracer_provider(trace_provider)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831, # Jaeger port, not for UI
)
span_processor = BatchSpanProcessor(jaeger_exporter) # Manage Jaeger
trace_provider.add_span_processor(span_processor)


@asynccontextmanager
async def lifespan(app: FastAPI):
    model["detector"] = ObjectDetectionServices("cpu") 
    yield
    model.clear()

# FastAPI
app = FastAPI(lifespan=lifespan)

FastAPIInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
# security = HTTPBasic()

@app.post("/ObjectDetection/detectObject", response_model=list[ObjectDetectionViewModel])
# async def detectObject(prompt: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)], data: UploadFile = File(...)): 
async def detectObject(prompt: str, data: UploadFile = File(...)): 
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