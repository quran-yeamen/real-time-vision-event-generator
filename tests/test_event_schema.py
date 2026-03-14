from src.event_schema import BoundingBox, DetectionEvent, ImageSize


def test_detection_event_creation():
    event = DetectionEvent(
        event_id="123",
        timestamp_utc="2026-03-14T12:00:00Z",
        pipeline_version="1.0.0",
        dataset_split="normal",
        video_source="Traffic2.mp4",
        frame_index=1,
        frame_time_seconds=0.033,
        object_class="car",
        class_id=2,
        confidence=0.95,
        bbox=BoundingBox(x1=10, y1=20, x2=100, y2=120),
        image_size=ImageSize(width=1280, height=720),
    )
    assert event.object_class == "car"
    assert event.bbox.x1 == 10