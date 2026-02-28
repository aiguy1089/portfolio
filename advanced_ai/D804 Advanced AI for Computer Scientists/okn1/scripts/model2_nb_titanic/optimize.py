# Simple sweep and timing for Naive Bayes Titanic (mostly baseline timing/metrics)
from pathlib import Path
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.naive_bayes import GaussianNB
from scripts.common.utils import ARTIFACTS_DIR, REPORTS_DIR, save_json

DATA_CSV = ARTIFACTS_DIR / "titanic" / "titanic.csv"

if __name__ == "__main__":
    df = pd.read_csv(DATA_CSV)
    target_col = "survived"
    y = df[target_col].astype(int)
    X = df.drop(columns=[target_col])

    cat_cols = X.select_dtypes(include=["object","bool","category"]).columns.tolist()
    num_cols = X.select_dtypes(exclude=["object","bool","category"]).columns.tolist()

    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ("num", "passthrough", num_cols),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # NB has few hyperparameters; we record timing and performance
    results = []
    for var_smoothing in [1e-9, 1e-8, 1e-7, 1e-6]:
        clf = GaussianNB(var_smoothing=var_smoothing)
        pipe = Pipeline([("pre", pre), ("clf", clf)])
        t0 = time.perf_counter()
        pipe.fit(X_train, y_train)
        train_time = time.perf_counter() - t0
        y_proba = pipe.predict_proba(X_test)[:, 1]
        y_pred = (y_proba >= 0.5).astype(int)
        metrics = {
            "var_smoothing": var_smoothing,
            "train_time_sec": train_time,
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "f1": float(f1_score(y_test, y_pred)),
            "roc_auc": float(roc_auc_score(y_test, y_proba)),
        }
        print(metrics)
        results.append(metrics)

    save_json({"trials": results}, REPORTS_DIR / "titanic_opt_results.json")
    print("Saved optimization results.")