import numpy as np
import cv2
# import secrets

from time import time
from loguru import logger
# from typing import Annotated
from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
from services.grounding_dino import ObjectDetectionServices
from model.object_detection_view_model import ObjectDetectionViewModel
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import psutil
from starlette.responses import Response

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

# Custom metrics
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP Requests', ['method', 'status', 'path'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'status', 'path'])
REQUEST_IN_PROGRESS = Gauge('http_requests_in_progress', 'HTTP Requests in progress', ['method', 'path'])

# System metrics
CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')

def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    method = request.method
    path = request.url.path

    REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()
    
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    status = response.status_code
    REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
    REQUEST_LATENCY.labels(method=method, status=status, path=path).observe(duration)
    REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

    return response


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
    
@app.get("/metrics")
async def metrics():
    update_system_metrics()
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)