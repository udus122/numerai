import os
import random
from pathlib import Path

import numpy as np

# Data directory
ROOT = Path(__file__).resolve().parents[3]
INPUT_ROOT = ROOT / "data"
RAW_DATA = INPUT_ROOT / "raw"
WORK_DIR = ROOT / "src"
OUTPUT_ROOT = ROOT / "out"
PROC_DATA = INPUT_ROOT / "prcessed"

# Set seed for reproducability
seed = 1234
random.seed(seed)
np.random.seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)
