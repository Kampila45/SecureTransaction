import pickle
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier


class ModelLoader:
    @staticmethod
    def load_model(model_path: str) -> Any:
        path = Path(model_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            model = GradientBoostingClassifier(n_estimators=10, random_state=42)
            X_dummy = np.array([[0.0, 0, 0, 0.0, 0.0]])
            y_dummy = np.array([0])
            model.fit(X_dummy, y_dummy)
            with open(path, "wb") as f:
                pickle.dump(model, f)
            return model
        if path.suffix == ".pkl":
            with open(path, "rb") as f:
                return pickle.load(f)
        elif path.suffix == ".joblib":
            return joblib.load(path)
        else:
            raise ValueError(f"Unsupported model format: {path.suffix}")

