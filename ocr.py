import easyocr
import warnings


# Keep OCR setup in one place so it can be reused by image/video/camera flows.
def build_reader(languages=None, use_gpu=True):
    if languages is None:
        languages = ["en"]

    # This warning is expected on CPU-only systems and is safe to ignore.
    warnings.filterwarnings(
        "ignore",
        message=".*pin_memory.*no accelerator is found.*",
        category=UserWarning,
    )

    return easyocr.Reader(languages, gpu=use_gpu)


# Read text boxes from a single frame (NumPy image from OpenCV).
def read_text(reader, frame):
    return reader.readtext(frame)
