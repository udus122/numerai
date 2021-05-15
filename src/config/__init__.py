import os
import random
from pathlib import Path
from pprint import pprint

import numpy as np

# Data directory
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
SRC_DIR = ROOT / "src"
OUTPUT_ROOT = ROOT / "out"
PROC_DATA = DATA_DIR / "prcessed"

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
