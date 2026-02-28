# Fetches Adult Income dataset and saves CSV (offline-friendly)
from pathlib import Path
import pandas as pd
from sklearn.datasets import fetch_openml

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "artifacts" / "adult"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_SOURCE = ROOT / "artifacts" / "sources" / "adult.csv"  # optional offline source

if __name__ == "__main__":
    csv_path = DATA_DIR / "adult.csv"
    if LOCAL_SOURCE.exists():
        print(f"Using local source: {LOCAL_SOURCE}")
        df = pd.read_csv(LOCAL_SOURCE)
        df.columns = [c.replace("-", "_") for c in df.columns]
        df.to_csv(csv_path, index=False)
        print(f"Saved to {csv_path}")
    else:
        try:
            print("Fetching Adult dataset from OpenML (ID: 1590)...")
            adult = fetch_openml("adult", version=2, as_frame=True)
            df = adult.frame
            df.columns = [c.replace("-", "_") for c in df.columns]
            df.to_csv(csv_path, index=False)
            print(f"Saved to {csv_path}")
        except Exception as e:
            print("Failed to fetch from OpenML. To run fully offline, place adult.csv at:")
            print(str(LOCAL_SOURCE))
            raise