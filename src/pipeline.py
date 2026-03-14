from pathlib import Path
import cv2

from src.detector import YoloRoadSceneDetector
from src.event_schema import BoundingBox, DetectionEvent, ImageSize
from src.logger import get_logger
from src.utils import append_jsonl, clear_file, generate_event_id, utc_now_iso
from src.video_io import VideoReader, VideoWriter


class VisionEventPipeline:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

        self.detector = YoloRoadSceneDetector(config["model_path"])
        self.confidence_threshold = config["confidence_threshold"]
        self.road_relevant_classes = set(config["road_relevant_classes"])
        self.input_root = Path(config["input_root"])
        self.output_events_dir = Path(config["output_events_dir"])
        self.output_videos_dir = Path(config["output_videos_dir"])
        self.save_annotated_video = config["save_annotated_video"]
        self.pipeline_version = config["pipeline_version"]
        self.supported_extensions = {
            ext.lower() for ext in config.get("supported_extensions", [".mp4"])
        }

    def run(self) -> None:
        video_files = self._discover_videos()

        if not video_files:
            self.logger.warning("No video files found under %s", self.input_root)
            return

        self.logger.info("Found %s video(s) to process.", len(video_files))

        for video_path in video_files:
            try:
                self.process_video(video_path)
            except Exception as exc:
                self.logger.exception("Failed to process %s: %s", video_path, exc)

        self.logger.info("Pipeline run complete.")

    def _discover_videos(self) -> list[Path]:
        all_files = self.input_root.rglob("*")
        return sorted(
            file_path for file_path in all_files
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions
        )

    def process_video(self, video_path: Path) -> None:
        dataset_split = video_path.parent.name
        video_name = video_path.stem

        output_jsonl = self.output_events_dir / dataset_split / f"{video_name}_events.jsonl"
        output_video = self.output_videos_dir / dataset_split / f"{video_name}_annotated.mp4"

        clear_file(output_jsonl)

        reader = VideoReader(str(video_path))
        writer = None

        if self.save_annotated_video:
            writer = VideoWriter(
                output_path=str(output_video),
                fps=reader.fps,
                width=reader.width,
                height=reader.height,
            )

        self.logger.info("Processing video: %s", video_path.name)

        frame_index = 0
        event_count = 0

        while True:
            success, frame = reader.read()
            if not success:
                break

            results = self.detector.detect(frame)

            for result in results:
                boxes = result.boxes
                if boxes is None:
                    continue

                for box in boxes:
                    class_id = int(box.cls[0].item())
                    confidence = float(box.conf[0].item())
                    class_name = result.names[class_id]

                    if class_name not in self.road_relevant_classes:
                        continue

                    if confidence < self.confidence_threshold:
                        continue

                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                    event = DetectionEvent(
                        event_id=generate_event_id(),
                        timestamp_utc=utc_now_iso(),
                        pipeline_version=self.pipeline_version,
                        dataset_split=dataset_split,
                        video_source=video_path.name,
                        frame_index=frame_index,
                        frame_time_seconds=round(frame_index / reader.fps, 3),
                        object_class=class_name,
                        class_id=class_id,
                        confidence=round(confidence, 4),
                        bbox=BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
                        image_size=ImageSize(width=reader.width, height=reader.height),
                    )

                    append_jsonl(output_jsonl, event.model_dump())
                    event_count += 1

                    if writer is not None:
                        label = f"{class_name} {confidence:.2f}"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(
                            frame,
                            label,
                            (x1, max(20, y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2,
                        )

            if writer is not None:
                writer.write(frame)

            frame_index += 1

        reader.release()
        if writer is not None:
            writer.release()

        self.logger.info(
            "Finished %s | frames=%s | events=%s",
            video_path.name,
            frame_index,
            event_count,
        )