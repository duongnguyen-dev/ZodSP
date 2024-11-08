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
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import set_meter_provider
from prometheus_fastapi_instrumentator import Instrumentator

class ResponseModel(BaseModel):
    response_data: list

model = {}

# # Traces using jeager
# trace_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "serving-grounding-dino"}))
# set_tracer_provider(trace_provider)

# jaeger_exporter = JaegerExporter(
#     agent_host_name="jaeger",
#     agent_port=6831, # Jaeger port, not for UI
# )
# span_processor = BatchSpanProcessor(jaeger_exporter) # Manage Jaeger
# trace_provider.add_span_processor(span_processor)



@asynccontextmanager
async def lifespan(app: FastAPI):
    model["detector"] = ObjectDetectionServices("cpu") 
    instrumentator = Instrumentator().instrument(app).expose(app, endpoint="/metrics")
    yield
    model.clear()

# FastAPI
app = FastAPI(lifespan=lifespan)
# FastAPIInstrumentor().instrument_app(app)
# RequestsInstrumentor().instrument()

@app.post("/detect", response_model=list[ObjectDetectionViewModel])
async def detectObject(prompt: str, data: UploadFile = File(...)): 
    start_time = time()
    labels = {"endpoint": "/detect"}

    try:
        image_bytes = await data.read()
        
        # Convert bytes data to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decode the image using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = model["detector"].predict(image, prompt)
        logger.info(f"{result}")
        elapsed_time = time() - start_time
        logger.info(f"Finished generate response: {elapsed_time:.2f} seconds")

        # Record metrics
        # request_counter.add(1, labels)
        # response_histogram.record(elapsed_time, labels)
        
        return result
    except Exception as error:
        logger.error(f"{error}")
        raise HTTPException(status_code=500, detail="Detection failed")