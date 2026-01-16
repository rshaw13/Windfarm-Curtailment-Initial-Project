import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from datetime import datetime, timezone


class MonotoneNonNegativeModel:
    """
    Wrapper around sklearn model that enforces:
      - monotone increasing predictions
      - non-negative outputs
    """

    def __init__(self, model):
        self.model = model

    def predict(self, X):
        """
        X must be shape (n_samples, 1)
        """
        y = self.model.predict(X)

        # Enforce monotonicity
        if len(y) > 1:
            y = np.maximum.accumulate(y)

        # Enforce non-negativity
        y = np.clip(y, 0, None)

        return y


def build_models(
    combined_dfs: dict,
    degree: int = 3,
    min_samples: int = 50
):
    """
    Build monotone, non-negative polynomial power curve models.

    Parameters
    ----------
    combined_dfs : dict[str, pd.DataFrame]
        Output of build_training_dataset()
        Must contain columns ['windspeed', 'output MW'].
    degree : int
        Polynomial degree (degrees of freedom control).
    min_samples : int
        Minimum samples required to train a model.

    Returns
    -------
    models : dict[str, MonotoneNonNegativeModel]
    metadata : dict[str, dict]
    """

    models = {}
    metadata = {}

    for wf, df in combined_dfs.items():

        sub = df.dropna(subset=["windspeed", "output MW"])
        if len(sub) < min_samples:
            continue

        X = sub["windspeed"].values.reshape(-1, 1)
        y = sub["output MW"].values

        # === BASE POLYNOMIAL MODEL ===
        base_model = make_pipeline(
            PolynomialFeatures(degree, include_bias=False),
            LinearRegression()
        )
        base_model.fit(X, y)

        # === WRAP WITH MONOTONIC ENFORCEMENT ===
        model = MonotoneNonNegativeModel(base_model)

        # === METRICS ===
        y_pred_raw = base_model.predict(X)
        r2 = r2_score(y, y_pred_raw)

        models[wf] = model
        metadata[wf] = {
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "degree": degree,
            "n_samples": int(len(sub)),
            "r2_score": round(float(r2), 4)
        }

    return models, metadata
