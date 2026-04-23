from pathlib import Path
import sys


# Add project package folder so this launcher works no matter where it is run from.
PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from main import main


# Backward-compatible entrypoint.
if __name__ == "__main__":
    main()