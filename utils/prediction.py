import pickle
import numpy as np
from pathlib import Path

def load_models(model_dir="models"):
    models = {}
    for pkl in Path(model_dir).glob("*.pkl"):
        with open(pkl, "rb") as f:
            models[pkl.stem] = pickle.load(f)
    return models

def predict(models, winds):
    output = {}
    for wf, ws in winds.items():
        if wf not in models:
            continue
        y = models[wf].predict(np.array([[ws]]))[0]
        output[wf] = max(0, y)
    return output
