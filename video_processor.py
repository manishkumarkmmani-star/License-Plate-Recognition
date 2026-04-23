import importlib
from pathlib import Path

from ocr import read_text
from plate_utils import extract_plate_candidates
from storage import append_plate, ensure_csv_header


def _load_cv2():
    try:
        return importlib.import_module("cv2")
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "OpenCV is required. Install it with: pip install opencv-python"
        ) from exc


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def is_image_source(source):
    if isinstance(source, (str, Path)):
        return Path(source).suffix.lower() in IMAGE_EXTENSIONS
    return False


def process_image(source, reader, csv_path, min_confidence=0.35, show=False, hold_on_finish=False):
    cv2 = _load_cv2()
    ensure_csv_header(csv_path)

    image = cv2.imread(str(source))
    if image is None:
        raise RuntimeError(f"Could not open image source: {source}")

    total_saved = 0
    seen = set()

    ocr_results = read_text(reader, image)
    plate_candidates = extract_plate_candidates(ocr_results, min_confidence=min_confidence)

    for plate_text, confidence in plate_candidates:
        if plate_text in seen:
            continue

        seen.add(plate_text)
        append_plate(csv_path, 0, plate_text, confidence)
        total_saved += 1
        print(f"Image: {plate_text} ({confidence:.2f})")

        if show:
            cv2.putText(
                image,
                plate_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

    if show:
        cv2.imshow("Plate OCR", image)
        if hold_on_finish:
            cv2.waitKey(0)
        else:
            cv2.waitKey(1)
        cv2.destroyAllWindows()

    return total_saved


# Process a video file (or camera stream) and store plate-like OCR results in CSV.
def process_video(
    source,
    reader,
    csv_path,
    every_n_frames=3,
    min_confidence=0.35,
    show=False,
    hold_on_finish=False,
    max_frames=0,
    log_every=30,
):
    cv2 = _load_cv2()
    ensure_csv_header(csv_path)

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")

    frame_index = 0
    total_saved = 0
    seen = set()
    last_frame = None
    processed_count = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            last_frame = frame.copy()

            # Skip frames to keep processing faster on normal laptops.
            if frame_index % max(every_n_frames, 1) != 0:
                frame_index += 1
                continue

            processed_count += 1
            if log_every > 0 and processed_count % log_every == 0:
                print(
                    f"Progress: processed {processed_count} frame(s), "
                    f"current frame index {frame_index}, saved {total_saved} plate(s)."
                )

            ocr_results = read_text(reader, frame)
            plate_candidates = extract_plate_candidates(ocr_results, min_confidence=min_confidence)

            for plate_text, confidence in plate_candidates:
                # Keep only first occurrence to reduce duplicate CSV rows.
                if plate_text in seen:
                    continue

                seen.add(plate_text)
                append_plate(csv_path, frame_index, plate_text, confidence)
                total_saved += 1
                print(f"Frame {frame_index}: {plate_text} ({confidence:.2f})")

                if show:
                    cv2.putText(
                        frame,
                        plate_text,
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )

            if show:
                cv2.imshow("Plate OCR", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            frame_index += 1

            if max_frames > 0 and frame_index >= max_frames:
                print(f"Reached max frame limit ({max_frames}). Stopping.")
                break

    finally:
        cap.release()
        if show:
            if hold_on_finish and last_frame is not None:
                cv2.putText(
                    last_frame,
                    "Done. Press any key to close.",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                cv2.imshow("Plate OCR", last_frame)
                cv2.waitKey(0)
            cv2.destroyAllWindows()

    return total_saved
