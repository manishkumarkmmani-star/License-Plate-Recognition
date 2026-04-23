# License Plate OCR

Detect plate-like text from image, video, or webcam using EasyOCR.
Results are saved to CSV.

## Requirements

- Python 3.9+
- pip

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install easyocr opencv-python
```

## Run

```bash
python main.py
python main.py --source input.mp4
python main.py --source test.jpg.jpg
python main.py --source 0
```

## Common Options

- `--source` input file path or camera index
- `--csv` output csv file (default: plates.csv)
- `--every-n-frames` process 1 frame every N frames
- `--min-confidence` OCR confidence threshold
- `--max-frames` stop after N frames
- `--show` preview window

Example:

```bash
python main.py --source input.mp4 --every-n-frames 3 --min-confidence 0.35 --show
```

## Output

CSV columns: frame_index, plate_text, confidence
