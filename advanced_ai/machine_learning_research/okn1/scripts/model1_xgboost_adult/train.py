# Train XGBoost on Adult Income
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import joblib
from scripts.common.utils import ARTIFACTS_DIR, REPORTS_DIR, save_json, time_block

DATA_CSV = ARTIFACTS_DIR / "adult" / "adult.csv"
MODEL_DIR = ARTIFACTS_DIR / "adult" / "model"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

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

    clf = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=4,
        eval_metric="logloss",
    )

    pipe = Pipeline([
        ("pre", pre),
        ("clf", clf),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    with time_block("Training"):
        pipe.fit(X_train, y_train)

    y_proba = pipe.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
    }

    save_json(metrics, REPORTS_DIR / "adult_metrics.json")
    joblib.dump(pipe, MODEL_DIR / "adult_xgb_pipeline.joblib")
    print("Saved model and metrics.")