# Loads Titanic dataset and saves CSV (offline-friendly)
from pathlib import Path
import pandas as pd

try:
    import seaborn as sns
except Exception:
    sns = None

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "artifacts" / "titanic"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOCAL_SOURCE = ROOT / "artifacts" / "sources" / "titanic.csv"  # optional offline source

if __name__ == "__main__":
    csv_path = DATA_DIR / "titanic.csv"
    if LOCAL_SOURCE.exists():
        print(f"Using local source: {LOCAL_SOURCE}")
        df = pd.read_csv(LOCAL_SOURCE)
    else:
        if sns is None:
            print("seaborn not available and no local source found. To run offline, place titanic.csv at:")
            print(str(LOCAL_SOURCE))
            raise SystemExit(1)
        print("Loading Titanic dataset from seaborn...")
        df = sns.load_dataset("titanic")
    # Basic column subset for consistency
    cols = [
        "survived","pclass","sex","age","sibsp","parch","fare","embarked",
        "class","who","adult_male","deck","embark_town","alone"
    ]
    df = df[cols]
    df.to_csv(csv_path, index=False)
    print(f"Saved to {csv_path}")