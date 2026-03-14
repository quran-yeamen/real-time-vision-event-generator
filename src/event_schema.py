from pydantic import BaseModel


class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class ImageSize(BaseModel):
    width: int
    height: int


class DetectionEvent(BaseModel):
    event_id: str
    timestamp_utc: str
    pipeline_version: str

    dataset_split: str
    video_source: str
    frame_index: int
    frame_time_seconds: float

    object_class: str
    class_id: int
    confidence: float

    bbox: BoundingBox
    image_size: ImageSize