# Evaluate saved XGBoost model on Adult Income test split (recomputes split deterministically)
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib
from scripts.common.utils import ARTIFACTS_DIR, REPORTS_DIR, save_json

DATA_CSV = ARTIFACTS_DIR / "adult" / "adult.csv"
MODEL_PATH = ARTIFACTS_DIR / "adult" / "model" / "adult_xgb_pipeline.joblib"

if __name__ == "__main__":
    df = pd.read_csv(DATA_CSV)
    target_col = "class"
    y = (df[target_col] == ">50K").astype(int)
    X = df.drop(columns=[target_col])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = joblib.load(MODEL_PATH)

    y_proba = pipe.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
    }

    # Save metrics
    save_json(metrics, REPORTS_DIR / "adult_metrics_eval.json")
    print(metrics)

    # Save confusion matrix image under reports/images
    images_dir = REPORTS_DIR / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(cm)
    fig, ax = plt.subplots(figsize=(4, 4))
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title("Adult Income – XGBoost Confusion Matrix")
    fig.tight_layout()
    out_path = images_dir / "adult_xgb_confusion_matrix.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)