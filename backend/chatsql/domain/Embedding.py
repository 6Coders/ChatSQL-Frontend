from dataclasses import dataclass

import numpy as np

@dataclass
class Embedding:
    text: str
    data: np.ndarray