# Simple hyperparameter tuning and timing for XGBoost Adult
from pathlib import Path
import time
import pandas as pd
import numpy as np
from itertools import product
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
from scripts.common.utils import ARTIFACTS_DIR, REPORTS_DIR, save_json

DATA_CSV = ARTIFACTS_DIR / "adult" / "adult.csv"

if __name__ == "__main__":
    df = pd.read_csv(DATA_CSV)
    target_col = "class"
    y = (df[target_col] == ">50K").astype(int)
    X = df.drop(columns=[target_col])

    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
    num_cols = X.select_dtypes(exclude=["object"]).columns.tolist()

    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ("num", "passthrough", num_cols),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    grid = {
        "n_estimators": [200, 400],
        "max_depth": [4, 6, 8],
        "learning_rate": [0.05, 0.1],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
    }

    trials = []
    for n_est, depth, lr, subs, cols in product(
        grid["n_estimators"], grid["max_depth"], grid["learning_rate"], grid["subsample"], grid["colsample_bytree"]
    ):
        clf = XGBClassifier(
            n_estimators=n_est,
            max_depth=depth,
            learning_rate=lr,
            subsample=subs,
            colsample_bytree=cols,
            random_state=42,
            n_jobs=4,
            eval_metric="logloss",
        )
        pipe = Pipeline([("pre", pre), ("clf", clf)])
        t0 = time.perf_counter()
        pipe.fit(X_train, y_train)
        train_time = time.perf_counter() - t0
        y_proba = pipe.predict_proba(X_test)[:, 1]
        y_pred = (y_proba >= 0.5).astype(int)
        metrics = {
            "n_estimators": n_est,
            "max_depth": depth,
            "learning_rate": lr,
            "subsample": subs,
            "colsample_bytree": cols,
            "train_time_sec": train_time,
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "f1": float(f1_score(y_test, y_pred)),
            "roc_auc": float(roc_auc_score(y_test, y_proba)),
        }
        print(metrics)
        trials.append(metrics)

    # Save all trials
    save_json({"trials": trials}, REPORTS_DIR / "adult_opt_results.json")
    print("Saved optimization results.")