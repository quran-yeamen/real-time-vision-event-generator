import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


def generate_event_id() -> str:
    return str(uuid.uuid4())


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def ensure_parent_dir(file_path: str | Path) -> None:
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)


def append_jsonl(file_path: str | Path, record: dict) -> None:
    ensure_parent_dir(file_path)
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


def clear_file(file_path: str | Path) -> None:
    ensure_parent_dir(file_path)
    Path(file_path).write_text("", encoding="utf-8")