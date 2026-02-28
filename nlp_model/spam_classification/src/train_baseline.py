from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

from data_prep import DataConfig, ensure_raw_dataset, preprocess_and_split


@dataclass
class ProjectConfig:
    random_seed: int
    data: dict
    features: dict
    model: dict
    reports: dict
    optimize: dict | None = None


def load_config(path: Path) -> ProjectConfig:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return ProjectConfig(**cfg)


def build_pipeline(cfg: ProjectConfig) -> Pipeline:
    tfidf_cfg = cfg.features.get("tfidf", {})
    vectorizer = TfidfVectorizer(
        ngram_range=tuple(tfidf_cfg.get("ngram_range", [1,1])),
        min_df=tfidf_cfg.get("min_df", 1),
        max_df=tfidf_cfg.get("max_df", 1.0),
        max_features=tfidf_cfg.get("max_features", None),
    )

    model_type = cfg.model.get("type", "logreg")
    if model_type == "logreg":
        mcfg = cfg.model.get("logreg", {})
        model = LogisticRegression(
            C=mcfg.get("C", 1.0),
            penalty=mcfg.get("penalty", "l2"),
            max_iter=mcfg.get("max_iter", 200),
            n_jobs=None,
        )
    else:
        raise ValueError("Only 'logreg' is implemented in baseline")

    return Pipeline([
        ("tfidf", vectorizer),
        ("model", model),
    ])


def evaluate_and_report(y_true, y_pred, labels, reports_dir: Path, metrics_path: Path, cm_path: Path) -> None:
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels, average='weighted', zero_division=0)
    metrics = {
        "accuracy": acc,
        "precision_weighted": precision,
        "recall_weighted": recall,
        "f1_weighted": f1,
    }
    reports_dir.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.tight_layout()
    plt.savefig(cm_path)
    plt.close()


if __name__ == "__main__":
    repo_root = Path(r"c:\Users\Admin\D803 QLN1 Task 2 Developing and Evaluating the Natural Language Processing Model")
    cfg_path = repo_root / "config" / "config.yaml"
    cfg = load_config(cfg_path)

    data_cfg = DataConfig(
        raw_path=repo_root / cfg.data["raw_path"],
        processed_train=repo_root / cfg.data["processed_train"],
        processed_test=repo_root / cfg.data["processed_test"],
        text_column=cfg.data["text_column"],
        label_column=cfg.data["label_column"],
        test_size=cfg.data.get("test_size", 0.2),
        lowercase=cfg.features.get("lowercase", True),
        remove_punct=cfg.features.get("remove_punct", True),
        remove_numbers=cfg.features.get("remove_numbers", False),
        remove_stopwords=cfg.features.get("remove_stopwords", True),
    )

    ensure_raw_dataset(data_cfg.raw_path)
    train_df, test_df = preprocess_and_split(data_cfg)

    pipe = build_pipeline(cfg)
    pipe.fit(train_df[data_cfg.text_column], train_df[data_cfg.label_column])
    preds = pipe.predict(test_df[data_cfg.text_column])

    reports_dir = repo_root / "reports"
    metrics_path = repo_root / cfg.reports["metrics_path"]
    cm_path = repo_root / cfg.reports["confusion_matrix_path"]

    labels = sorted(train_df[data_cfg.label_column].unique().tolist())
    evaluate_and_report(test_df[data_cfg.label_column], preds, labels, reports_dir, metrics_path, cm_path)

    # Save model
    import joblib
    model_path = repo_root / "models" / "baseline_model.joblib"
    joblib.dump(pipe, model_path)
    print(f"Saved model to {model_path}")
    print(f"Metrics at {metrics_path} and confusion matrix at {cm_path}")