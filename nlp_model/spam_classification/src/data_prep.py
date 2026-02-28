from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import urllib.request
import zipfile
import io
import pandas as pd
from sklearn.model_selection import train_test_split

from utils import basic_clean, remove_stop_words


SMS_SPAM_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"


@dataclass
class DataConfig:
    raw_path: Path
    processed_train: Path
    processed_test: Path
    text_column: str
    label_column: str
    test_size: float = 0.2
    lowercase: bool = True
    remove_punct: bool = True
    remove_numbers: bool = False
    remove_stopwords: bool = True


def ensure_raw_dataset(raw_path: Path) -> None:
    if raw_path.exists():
        return
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    # Download zip into memory, extract SMSSpamCollection
    print("Downloading SMS Spam Collection dataset...")
    with urllib.request.urlopen(SMS_SPAM_URL) as resp:
        data = resp.read()
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        with zf.open("SMSSpamCollection") as f:
            # File is tab-separated: label \t text
            lines = f.read().decode("utf-8", errors="ignore").splitlines()
    labels, texts = [], []
    for line in lines:
        if "\t" not in line:
            continue
        lab, txt = line.split("\t", 1)
        labels.append(lab.strip())
        texts.append(txt.strip())
    df = pd.DataFrame({"label": labels, "text": texts})
    df.to_csv(raw_path, index=False)
    print(f"Saved raw dataset to {raw_path}")


def preprocess_and_split(cfg: DataConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(cfg.raw_path)

    # Basic cleaning
    df[cfg.text_column] = df[cfg.text_column].astype(str).map(
        lambda t: basic_clean(
            t,
            lowercase=cfg.lowercase,
            remove_punct=cfg.remove_punct,
            remove_numbers=cfg.remove_numbers,
        )
    )

    if cfg.remove_stopwords:
        df[cfg.text_column] = remove_stop_words(df[cfg.text_column].tolist())

    train_df, test_df = train_test_split(
        df, test_size=cfg.test_size, random_state=42, stratify=df[cfg.label_column]
    )

    cfg.processed_train.parent.mkdir(parents=True, exist_ok=True)
    cfg.processed_test.parent.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(cfg.processed_train, index=False)
    test_df.to_csv(cfg.processed_test, index=False)
    print(f"Wrote {cfg.processed_train} and {cfg.processed_test}")
    return train_df, test_df


if __name__ == "__main__":
    # Allow running standalone with defaults in config/config.yaml if desired
    print("This module is intended to be used by train scripts.")