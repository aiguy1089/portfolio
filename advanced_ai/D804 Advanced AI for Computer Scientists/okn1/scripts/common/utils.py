import time
import json
from pathlib import Path
from typing import Any, Dict

ARTIFACTS_DIR = Path(__file__).resolve().parents[2] / "artifacts"
REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def save_json(data: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def time_block(label: str):
    class _Timer:
        def __enter__(self):
            self.start = time.perf_counter()
            return self
        def __exit__(self, exc_type, exc, tb):
            self.elapsed = time.perf_counter() - self.start
            print(f"{label} took {self.elapsed:.3f}s")
    return _Timer()