from ultralytics import YOLO


class YoloRoadSceneDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect(self, frame):
        return self.model(frame, verbose=False)