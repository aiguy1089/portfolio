# D803 — QLN1 Task 2: NLP Model (Minimal Submission)

This branch contains only the files required to run the NLP pipeline for SMS spam classification.

## Required files
- config/config.yaml
- src/data_prep.py
- src/train_baseline.py
- src/train_optimize.py
- src/utils.py
- requirements.txt

## How to run
1. Create a virtual environment and install dependencies:
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
```
2. Train baseline and generate metrics + confusion matrix:
```powershell
py -3 src/train_baseline.py
```
3. Run hyperparameter search (optional):
```powershell
py -3 src/train_optimize.py
```

Artifacts (metrics, confusion matrix, model) are written to `reports/` and `models/` when you run the scripts locally.