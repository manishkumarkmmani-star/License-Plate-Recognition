import argparse
from pathlib import Path

from ocr import build_reader
from video_processor import is_image_source, process_image, process_video


# Parse CLI arguments so the script is easy to run and share on GitHub.
def parse_args():
    parser = argparse.ArgumentParser(description="Extract plate-like text from video and store to CSV")

    parser.add_argument(
        "--source",
        default="input.mp4",
        help='Video file path, or camera index like "0"',
    )
    parser.add_argument(
        "--csv",
        default="plates.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--every-n-frames",
        type=int,
        default=3,
        help="Process one frame every N frames",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.35,
        help="Minimum OCR confidence",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show preview window while processing",
    )
    parser.add_argument(
        "--hold-on-finish",
        action="store_true",
        help="Keep final preview frame open until a key is pressed",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=0,
        help="Stop after this many frames (0 means no limit)",
    )
    parser.add_argument(
        "--log-every",
        type=int,
        default=30,
        help="Print processing progress every N processed frames",
    )

    return parser.parse_args()


# Convert source to camera index if user passed digits like "0".
def parse_source(raw_source, base_dir):
    if raw_source.isdigit():
        return int(raw_source)

    source_path = Path(raw_source)
    if not source_path.is_absolute():
        source_path = base_dir / source_path
    return str(source_path)


def resolve_csv_path(raw_csv, base_dir):
    csv_path = Path(raw_csv)
    if not csv_path.is_absolute():
        csv_path = base_dir / csv_path
    return csv_path


def main():
    args = parse_args()

    base_dir = Path(__file__).resolve().parent

    source = parse_source(args.source, base_dir)
    csv_path = resolve_csv_path(args.csv, base_dir)

    reader = build_reader(languages=["en"], use_gpu=False)

    if is_image_source(source):
        total_saved = process_image(
            source=source,
            reader=reader,
            csv_path=csv_path,
            min_confidence=args.min_confidence,
            show=args.show,
            hold_on_finish=args.hold_on_finish,
        )
    else:
        total_saved = process_video(
            source=source,
            reader=reader,
            csv_path=csv_path,
            every_n_frames=args.every_n_frames,
            min_confidence=args.min_confidence,
            show=args.show,
            hold_on_finish=args.hold_on_finish,
            max_frames=args.max_frames,
            log_every=args.log_every,
        )

    print(f"Saved {total_saved} unique plate(s) to: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
