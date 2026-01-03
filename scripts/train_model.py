import pickle
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb

try:
    import kagglehub
except ImportError:
    kagglehub = None


def load_sample_data() -> tuple[np.ndarray, np.ndarray]:
    np.random.seed(42)
    n_samples = 10000
    
    amount = np.random.uniform(10, 10000, n_samples)
    hour = np.random.randint(0, 24, n_samples)
    day_of_week = np.random.randint(0, 7, n_samples)
    has_ip = np.random.choice([0, 1], n_samples)
    has_device = np.random.choice([0, 1], n_samples)
    
    X = np.column_stack([amount, hour, day_of_week, has_ip, has_device])
    
    fraud_prob = (
        (amount > 5000) * 0.3 +
        (hour < 6) * 0.2 +
        (hour > 22) * 0.15 +
        np.random.uniform(0, 0.2, n_samples)
    )
    y = (fraud_prob > 0.5).astype(int)
    
    return X, y


def load_kaggle_credit_card_data() -> tuple[np.ndarray, np.ndarray] | None:
    try:
        import pandas as pd
        
        if kagglehub is None:
            csv_path = Path("creditcard.csv")
            if not csv_path.exists():
                return None
        else:
            print("Downloading Kaggle dataset...")
            dataset_path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
            csv_path = Path(dataset_path) / "creditcard.csv"
            if not csv_path.exists():
                csv_files = list(Path(dataset_path).glob("*.csv"))
                if csv_files:
                    csv_path = csv_files[0]
                else:
                    return None
        
        print(f"Loading data from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        amount_col = df["Amount"].values.reshape(-1, 1)
        time_col = df["Time"].values
        
        hour = (time_col % (24 * 3600) // 3600).reshape(-1, 1)
        day_of_week = ((time_col // (24 * 3600)) % 7).reshape(-1, 1)
        
        has_ip = np.ones((len(df), 1))
        has_device = np.ones((len(df), 1))
        
        X_custom = np.column_stack([amount_col, hour, day_of_week, has_ip, has_device])
        
        y = df["Class"].values
        
        return X_custom, y
    except Exception as e:
        print(f"Error loading Kaggle dataset: {e}")
        return None


def train_xgboost_model(X_train: np.ndarray, y_train: np.ndarray) -> xgb.XGBClassifier:
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss",
    )
    model.fit(X_train, y_train)
    return model


def train_gradient_boosting_model(
    X_train: np.ndarray, y_train: np.ndarray
) -> GradientBoostingClassifier:
    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model: xgb.XGBClassifier | GradientBoostingClassifier, X_test: np.ndarray, y_test: np.ndarray) -> None:
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")


def main() -> None:
    print("Loading data...")
    data = load_kaggle_credit_card_data()
    if data is None:
        print("Kaggle dataset not found, using sample data...")
        X, y = load_sample_data()
    else:
        X, y = data
        print(f"Loaded {len(X)} samples from Kaggle dataset")
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training XGBoost model...")
    model = train_xgboost_model(X_train, y_train)
    
    print("Evaluating model...")
    evaluate_model(model, X_test, y_test)
    
    model_path = Path("app/adapters/outbound/ml/models/model.pkl")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving model to {model_path}...")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print("Model training complete!")


if __name__ == "__main__":
    main()

