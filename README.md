# Real-Time Driver Scene Event Generator

A computer vision pipeline that processes **driver point-of-view road video** and converts detections into **structured JSON events** for downstream data engineering and analytics.

---

## Overview

This project is **Phase 1** of a larger end-to-end portfolio pipeline.

It takes raw driving footage, runs object detection with **YOLOv8**, filters for road-scene entities, and produces a machine-readable **JSONL event stream** that captures what happened in each frame.

The output of this repository is not just annotated video — it is **structured event data** designed to feed the next phase of the system.

---

## What This Project Does

The pipeline:

1. Reads driver POV video files  
2. Runs object detection using **YOLOv8**  
3. Identifies relevant road-scene objects  
4. Converts detections into structured event records  
5. Saves those records as **JSONL files**  
6. Produces annotated output videos for visual validation  

### Objects Detected

- Cars
- Trucks
- Buses
- Motorcycles
- Pedestrians
- Bicycles
- Traffic lights
- Stop signs

---

## Pipeline Flow

```text
Driver POV Video
      ↓
YOLOv8 Detection
      ↓
Road Scene Objects Identified
      ↓
Structured Detection Events
      ↓
JSONL Event Stream
```

These JSONL files act as the **raw event layer** for downstream ingestion, storage, and analytics.

---

## Example Event Output

Each detection is transformed into a structured event record like this:

```json
{
  "event_id": "9e2e7f8e",
  "timestamp_utc": "2026-03-14T14:21:00Z",
  "pipeline_version": "1.0.0",
  "dataset_split": "normal",
  "video_source": "Traffic2.mp4",
  "frame_index": 134,
  "frame_time_seconds": 4.47,
  "object_class": "car",
  "class_id": 2,
  "confidence": 0.91
}
```

This event structure makes the output easy to ingest into cloud pipelines, validate, transform, and analyze later.

---

## Project Structure

```text
real-time-vision-event-generator/
│
├── src/
│   ├── detector.py
│   ├── pipeline.py
│   ├── event_schema.py
│   ├── video_io.py
│   ├── utils.py
│   └── main.py
│
├── configs/
│   └── pipeline_config.yaml
│
├── tests/
│
├── data/
│   └── raw/
│       ├── normal/
│       └── edge_cases/
│
└── outputs/
    ├── events/
    ├── videos/
    └── logs/
```

---

## Running the Pipeline

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the project

```bash
python -m src.main
```

### Output generated

Running the pipeline will:

- Scan the `data/raw` directory for video files
- Run YOLOv8 object detection
- Generate structured detection events
- Save results to `outputs/events`
- Create annotated videos in `outputs/videos`

---

## How This Connects to Phase 2

This repository focuses on **event generation**.

The JSONL files produced here are intended to become the input source for **Phase 2**, where the raw event stream will move into a cloud-based ingestion pipeline.

```text
Detection Events (JSONL)
          ↓
Azure Data Ingestion Pipeline
          ↓
Azure Data Lake Storage
          ↓
Data Transformation and Analytics
```

This separation is intentional.

Phase 1 handles **computer vision and event creation**.  
Phase 2 will handle **cloud ingestion and raw data storage**.

That design mirrors how real-world systems are built: one layer generates operational data, and the next layer moves it into scalable analytics infrastructure.

---

## Technologies Used

- Python
- YOLOv8 (Ultralytics)
- OpenCV
- Pydantic
- PyTest
- GitHub Actions

---

## Why This Project Matters

This project demonstrates how computer vision output can be turned into **structured engineering data** instead of staying trapped inside a model or notebook.

It shows the first step in a larger architecture:

- **Phase 1:** Generate structured road-scene events from video  
- **Phase 2:** Ingest raw events into Azure storage  
- **Phase 3:** Transform and model the data for analytics and dashboards  

