import re


# This regex is intentionally simple: it keeps common plate-like alphanumeric strings.
PLATE_PATTERN = re.compile(r"^[A-Z0-9]{5,10}$")


# Normalize OCR text so noisy spacing/symbols do not break matching.
def normalize_text(text):
    cleaned = re.sub(r"[^A-Za-z0-9]", "", text).upper()
    return cleaned


# Convert OCR output into plate candidates: (plate_text, confidence).
def extract_plate_candidates(ocr_results, min_confidence=0.35):
    candidates = []

    for _, text, confidence in ocr_results:
        if confidence < min_confidence:
            continue

        plate_text = normalize_text(text)
        if not plate_text:
            continue

        if PLATE_PATTERN.match(plate_text):
            candidates.append((plate_text, float(confidence)))

    return candidates
