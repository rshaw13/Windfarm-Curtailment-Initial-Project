import json
from pathlib import Path
from datetime import datetime, timezone

TRAINING_WINDOW_FILE = Path("data/training_window.json")
MODEL_METADATA_FILE = Path("metadata/model_metadata.json")

TRAINING_WINDOW_FILE.parent.mkdir(exist_ok=True)
MODEL_METADATA_FILE.parent.mkdir(exist_ok=True)

def save_training_window(first_date, last_date):
    data = {
        "first_date": first_date,
        "last_date": last_date,
        "trained_at": datetime.now(timezone.utc).isoformat()
    }
    with open(TRAINING_WINDOW_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_model_metadata(metadata: dict):
    with open(MODEL_METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)
