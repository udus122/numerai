import os
import random
from pathlib import Path
from pprint import pprint

import numpy as np

# Data directory
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "output"
SRC_DIR = ROOT_DIR / "src"
LOG_DIR = ROOT_DIR / "logs"
MODEL_DIR = ROOT_DIR / "models"


# Set seed for reproducability
seed = 1234
random.seed(seed)
np.random.seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)

# Numerai
NUMERAI_PUBLIC = os.environ.get("NUMERAI_PUBLIC")
NUMERAI_SECRET = os.environ.get("NUMERAI_SECRET")

if __name__ == "__main__":
    pprint(globals())
