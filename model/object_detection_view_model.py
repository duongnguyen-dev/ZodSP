from pydantic import BaseModel

class ObjectDetectionViewModel(BaseModel):
    response_data: list