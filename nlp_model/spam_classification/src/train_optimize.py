from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import yaml

from data_prep import DataConfig, ensure_raw_dataset, preprocess_and_split


def load_config(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    repo_root = Path(r"c:\Users\Admin\D803 QLN1 Task 2 Developing and Evaluating the Natural Language Processing Model")
    cfg = load_config(repo_root / "config" / "config.yaml")

    data_cfg = DataConfig(
        raw_path=repo_root / cfg["data"]["raw_path"],
        processed_train=repo_root / cfg["data"]["processed_train"],
        processed_test=repo_root / cfg["data"]["processed_test"],
        text_column=cfg["data"]["text_column"],
        label_column=cfg["data"]["label_column"],
        test_size=cfg["data"].get("test_size", 0.2),
        lowercase=cfg["features"].get("lowercase", True),
        remove_punct=cfg["features"].get("remove_punct", True),
        remove_numbers=cfg["features"].get("remove_numbers", False),
        remove_stopwords=cfg["features"].get("remove_stopwords", True),
    )

    ensure_raw_dataset(data_cfg.raw_path)
    train_df, test_df = preprocess_and_split(data_cfg)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("model", LogisticRegression(max_iter=300)),
    ])

    grid = cfg["optimize"]["param_grid"]
    # Ensure tuples for ngram_range (sklearn requires tuples, not lists)
    if "tfidf__ngram_range" in grid:
        grid["tfidf__ngram_range"] = [tuple(v) for v in grid["tfidf__ngram_range"]]

    cv = cfg["optimize"].get("cv_folds", 5)
    n_jobs = cfg["optimize"].get("n_jobs", -1)

    search = GridSearchCV(pipe, grid, cv=cv, n_jobs=n_jobs, verbose=1)
    search.fit(train_df[data_cfg.text_column], train_df[data_cfg.label_column])

    best_params_path = repo_root / "reports" / "best_params.json"
    best_params_path.parent.mkdir(parents=True, exist_ok=True)
    with open(best_params_path, "w", encoding="utf-8") as f:
        json.dump({"best_params": search.best_params_, "best_score_cv": search.best_score_}, f, indent=2)
    print(f"Saved best params to {best_params_path}")