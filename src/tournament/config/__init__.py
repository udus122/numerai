import os
import random

import numpy as np

# Data directory
DIR = "/kaggle/working"

# Set seed for reproducability
seed = 1234
random.seed(seed)
np.random.seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)
