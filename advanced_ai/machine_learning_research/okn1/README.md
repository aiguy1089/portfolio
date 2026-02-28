# D804 OKN1 Task 1 - Using AI to Resolve Challenges

This project contains two models and optimization per the assessment:

- Model 1 (Advanced): XGBoost on Adult Income (classification)
- Model 2 (Probabilistic): Naive Bayes on Titanic (classification)
- Optimization: Hyperparameter tuning and efficiency benchmarks for both

## Structure
- scripts/common: shared utilities
- scripts/model1_xgboost_adult: data prep, train, eval for Model 1
- scripts/model2_nb_titanic: data prep, train, eval for Model 2
- scripts/deploy: example FastAPI deployment stubs
- artifacts: saved models, metrics, plots
- reports: benchmark and validation outputs
- submission: draft paper and branch history helpers

## Quick start (Cloud Academy Lab)
1. Python 3.10+
2. `pip install -r requirements.txt`
3. Model 1
   - `python scripts/model1_xgboost_adult/fetch_data.py`
   - `python scripts/model1_xgboost_adult/train.py`
   - `python scripts/model1_xgboost_adult/evaluate.py`
4. Model 2
   - `python scripts/model2_nb_titanic/fetch_data.py`
   - `python scripts/model2_nb_titanic/train.py`
   - `python scripts/model2_nb_titanic/evaluate.py`
5. Optimization & benchmarks
   - `python scripts/model1_xgboost_adult/optimize.py`
   - `python scripts/model2_nb_titanic/optimize.py`
6. Export branch history
   - `git log --pretty=format:"%h | %ad | %an | %s" --date=short --decorate --graph --all > submission/branch_history.txt`

## Deployment plan (high level)
- Package the trained model and preprocessing pipeline
- Expose `predict` via FastAPI (see scripts/deploy)
- Containerize (optional), then deploy to a service

## Naming per brief
- Model names: `D804_PA_Model_AdultIncome_XGB` and `D804_PA_Model_Titanic_NB`
- Optimization names: `D804_PA_Optimization_AdultIncome_XGB` and `D804_PA_Optimization_Titanic_NB`