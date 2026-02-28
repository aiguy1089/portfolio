# D804 OKN1 Task 1 - Using AI to Resolve Challenges

This project contains two models and optimization per the assessment:

- Model 1 (Advanced): XGBoost on Adult Income (classification)
- Model 2 (Probabilistic): Naive Bayes on Titanic (classification)
- Optimization: Hyperparameter tuning and efficiency benchmarks for both

## Structure (minimal for assessment)
- scripts/common: shared utilities
- scripts/model1_xgboost_adult: data prep, train, eval, optimize for Model 1
- scripts/model2_nb_titanic: data prep, train, eval, optimize for Model 2
- requirements.txt
- README.md

## Quick start (Cloud Academy Lab)
1. Python 3.10+
2. `pip install -r requirements.txt`
3. Model 1
   - `python -m scripts.model1_xgboost_adult.fetch_data`
   - `python -m scripts.model1_xgboost_adult.train`
   - `python -m scripts.model1_xgboost_adult.evaluate`
4. Model 2
   - `python -m scripts.model2_nb_titanic.fetch_data`
   - `python -m scripts.model2_nb_titanic.train`
   - `python -m scripts.model2_nb_titanic.evaluate`
5. Export branch history (run in repo root)
   - `git log --pretty=format:"%h | %ad | %an | %s" --date=short --decorate --graph --all > branch_history.txt`

## Deployment plan (high level)
- Package the trained model and preprocessing pipeline
- Expose `predict` via FastAPI (see scripts/deploy)
- Containerize (optional), then deploy to a service

## Naming per brief
- Model names: `D804_PA_Model_AdultIncome_XGB` and `D804_PA_Model_Titanic_NB`
- Optimization names: `D804_PA_Optimization_AdultIncome_XGB` and `D804_PA_Optimization_Titanic_NB`