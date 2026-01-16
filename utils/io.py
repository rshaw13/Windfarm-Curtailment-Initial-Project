import pickle
from pathlib import Path

def save_models(models, model_dir="models"):
    Path(model_dir).mkdir(exist_ok=True)
    for name, model in models.items():
        with open(Path(model_dir) / f"{name}.pkl", "wb") as f:
            pickle.dump(model, f)

def save_live_state(df, path):
    df.to_parquet(path, index=False)
