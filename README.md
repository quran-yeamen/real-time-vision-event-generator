# Real-Time Driver Scene Event Generator

## Overview

This project is a computer vision pipeline that processes **driver point-of-view road videos** and converts visual detections into **structured event data**.

Using **YOLOv8**, the system detects objects commonly encountered while driving, such as:

- cars
- trucks
- buses
- motorcycles
- pedestrians
- bicycles
- traffic lights
- stop signs

Each detection is transformed into a **structured JSON event**, creating a machine-readable event stream that represents what occurred in the driving scene.

This repository represents **Phase 1** of a larger data engineering pipeline.

---

# What This Project Does

The pipeline performs the following steps:

1. Reads driver POV video files
2. Runs object detection using YOLOv8
3. Filters detections relevant to road environments
4. Converts detections into structured event records
5. Saves events as JSONL files for downstream processing
6. Generates annotated output videos for visual validation

Pipeline flow:

Driver POV Video
↓
YOLOv8 Detection
↓
Road Scene Objects Identified
↓
Structured Detection Events
↓
JSONL Event Stream


These JSONL files act as **raw event data** that can be processed by downstream data systems.

---

# Example Event Output

Each detection becomes a structured event record:

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
These events form the raw dataset for further analytics and data processing.
```json

real-time-vision-event-generator
│
├── src
│   ├── detector.py
│   ├── pipeline.py
│   ├── event_schema.py
│   ├── video_io.py
│   ├── utils.py
│   └── main.py
│
├── configs
│   └── pipeline_config.yaml
│
├── tests
│
├── data
│   └── raw
│       ├── normal
│       └── edge_cases
│
└── outputs
    ├── events
    ├── videos
    └── logs
```

Running the Pipeline

Install dependencies:

pip install -r requirements.txt

Run the pipeline:

python -m src.main

The pipeline will:

scan the data/raw directory for videos

run YOLOv8 object detection

generate detection events

store results in outputs/events

create annotated output videos

How This Connects to Phase 2

This project focuses on event generation.

The JSONL event files produced here will become the input data source for Phase 2.

Phase 2 will introduce a cloud ingestion pipeline that:

Detection Events (JSONL)
        ↓
Azure Data Ingestion Pipeline
        ↓
Azure Data Lake Storage
        ↓
Data Transformation and Analytics

By separating event generation from data ingestion, the system mirrors how many real-world data pipelines are structured.

Technologies Used

Python

YOLOv8 (Ultralytics)

OpenCV

Pydantic

PyTest

GitHub Actions


---

### Why this version is better for your repo

It:

- focuses on **what this project does**
- shows **clear pipeline purpose**
- introduces **Phase 2 naturally**
- avoids overexplaining the entire system
- reads like a **real engineering project description**

---

If you want, I can also show you **one tiny README upgrade that makes the repo look significantly mo
