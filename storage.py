import csv
from pathlib import Path


# Ensure the CSV exists and has headers once.
def ensure_csv_header(csv_path):
    path = Path(csv_path)

    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["frame_index", "plate_text", "confidence"])


# Append a single detection row.
def append_plate(csv_path, frame_index, plate_text, confidence):
    path = Path(csv_path)

    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([frame_index, plate_text, f"{confidence:.4f}"])
