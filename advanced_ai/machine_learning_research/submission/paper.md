# Using AI to Resolve Challenges: Two Mini-Projects for D804 OKN1

## Introduction
This paper presents two AI mini-projects aligned with the competencies of the D804 OKN1 assessment: (1) an advanced model using XGBoost on the Adult Income dataset, and (2) a probabilistic model using Naive Bayes on the Seaborn Titanic dataset. Each project includes data preparation, model training, validation, and an outline for deployment. Optimization work demonstrates performance tuning and evaluation benchmarks.

## Model 1: D804_PA_Model_AdultIncome_XGB
### Goal
Predict whether an individual’s income exceeds $50K based on census attributes.

### Dataset
- Source: OpenML “adult” (ID: 1590). Offline fallback supported via local CSV.
- Features: Mixed categorical (e.g., workclass, education, occupation) and numerical (e.g., age, hours-per-week, capital-gain).
- Target: income (>50K or <=50K).

### Why This Dataset
- Well-known benchmark for tabular classification and fairness considerations.
- Sufficient size and feature diversity to showcase advanced tree-based modeling.

### Data Preparation
- Standardized column names (replace hyphens with underscores).
- Train/validation split (stratified by target) and basic preprocessing in the training script, including:
  - Handling missing values.
  - One-hot encoding for categorical variables.
  - Keeping numerical features as-is.

### Method and Development
- Advanced method: Gradient-boosted decision trees using XGBoost.
- Scripts: fetch_data.py, train.py, evaluate.py, optimize.py.
- Training includes reasonable defaults for depth, learning rate, estimators, and early stopping where supported.

### Training and Validation
- Metrics: accuracy, precision, recall, F1 (macro and weighted), ROC-AUC where applicable.
- Validation via a held-out split; cross-validation can be enabled in optimization.

### Deployment Plan
- Package preprocessing (encoder) and model into a pipeline object.
- Expose predict endpoint using FastAPI.
- Containerize and deploy to a service platform; monitor latency and accuracy.

## Model 2: D804_PA_Model_Titanic_NB
### Goal
Predict passenger survival from the Titanic dataset using a probabilistic approach.

### Dataset
- Source: Seaborn’s titanic dataset. Offline fallback via local CSV.
- Features subset: survived, pclass, sex, age, sibsp, parch, fare, embarked, class, who, adult_male, deck, embark_town, alone.
- Target: survived (0/1).

### Why This Dataset
- Classic probabilistic modeling example with mixed data types and missingness.
- Clear interpretability for demonstrating Naive Bayes assumptions.

### Data Preparation
- Column subset selection for consistency.
- Imputation of missing values; encoding of categorical variables.

### Method and Development
- Probabilistic method: Naive Bayes (e.g., GaussianNB after encoding/imputation, or CategoricalNB where feasible).
- Scripts: fetch_data.py, train.py, evaluate.py, optimize.py.

### Training and Validation
- Metrics: accuracy, precision, recall, F1 (macro and weighted), ROC-AUC (if probabilities available).
- Held-out validation split.

### Deployment Plan
- Persist preprocessing and NB model.
- Provide a lightweight API endpoint for batch and single predictions.

## Optimization and Evaluation
### Project Names
- D804_PA_Optimization_AdultIncome_XGB
- D804_PA_Optimization_Titanic_NB

### Actions Performed
- Hyperparameter tuning (learning rate, max_depth, n_estimators for XGB; smoothing/prior settings for NB).
- Efficiency measurements (fit time, predict time) on held-out sets.
- Benchmarks: selected metrics (F1/accuracy), confusion matrix, and timing summaries.

## Professional Practice and Tools
- Code is documented and organized into clear scripts with offline-friendly data loaders.
- Reproducibility: requirements.txt and README instructions.
- Branch management: commit messages for each assessment part; branch history to be exported when ready.

## References (APA style)
- Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. https://doi.org/10.1145/2939672.2939785
- Dua, D., & Graff, C. (2017). UCI Machine Learning Repository: Adult Data Set. https://archive.ics.uci.edu/ml/datasets/adult
- Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825–2830.
- Waskom, M. (2021). Seaborn: Statistical Data Visualization. Journal of Open Source Software, 6(60), 3021.

## Conclusion
These two mini-projects demonstrate the preparation, modeling, validation, and optimization of AI systems using both advanced (XGBoost) and probabilistic (Naive Bayes) techniques. The codebase is structured for clarity and reproducibility, and the deployment path is defined for production handoff. This work aligns with the competencies of the performance assessment and is ready for submission and further extension.