# D803 — QLN1 Task 2: Developing and Evaluating the NLP Model

Author: [Your Name]
Date: [Date]
Course: Natural Language Processing — D803

---

## C. Libraries and Tools

This project was implemented in Python 3.13 using a lightweight, classical NLP stack centered on scikit-learn. Text features were extracted with TF–IDF to capture informative unigrams and bigrams, which is a well-supported approach for short-text classification tasks and competitive baselines [@Xiao2024TFIDFWord2Vec; @MDPI2024TextClassificationReview]. NLTK provided the English stopword list for normalization, while pandas and NumPy handled data loading and efficient tabular/numerical operations.

For experiment management and outputs, scikit-learn supplied model training, evaluation metrics, and cross-validation; models were persisted with joblib and plots (e.g., the confusion matrix) were produced with matplotlib/seaborn. A YAML configuration file (`config/config.yaml`) centralizes data paths, preprocessing flags, TF–IDF settings, and hyperparameters to ensure reproducibility and easy re-runs in VS Code.

## D. System Implementation

The system addresses binary SMS classification (spam vs. ham) using the public SMS Spam Collection. Data are downloaded on first run and cached locally [@Alsaeedi2022SpamSurvey]. Preprocessing normalizes text through lowercasing, punctuation removal, and optional number removal, followed by stopword filtering with NLTK. We then create a stratified 80/20 train/test split to preserve class balance across splits.

Features are generated via TF–IDF over unigrams and bigrams with configurable document-frequency thresholds, which is effective for short texts [@Xiao2024TFIDFWord2Vec]. A regularized Logistic Regression classifier (L2) serves as the baseline due to its speed, interpretability, and strong performance on sparse vector spaces in short-text tasks [@Shyrokykh2023ShortText; @MDPI2024TextClassificationReview]. The pipeline trains on the training set and evaluates on the held-out test set, saving the model, metrics, and confusion matrix to the `models/` and `reports/` directories to ensure reproducibility.

Implementation is organized into small, testable scripts: `src/data_prep.py` handles download/splitting and cleaning; `src/train_baseline.py` fits and evaluates the baseline and writes artifacts; and `src/train_optimize.py` performs hyperparameter search for TF–IDF and Logistic Regression. Utility functions in `src/utils.py` centralize text normalization, while configuration in `config/config.yaml` controls paths and toggles for repeatable runs.

Repository structure:
```
config/config.yaml
data/raw/sms_spam.csv
data/processed/train.csv, test.csv
models/baseline_model.joblib
reports/metrics.json, confusion_matrix.png, best_params.json
src/*.py
```

## E. Evaluation Summary

On the held-out test set, the model achieved 0.984 accuracy, 0.984 weighted precision, 0.984 weighted recall, and a 0.983 weighted F1 score (see `reports/metrics.json`). These results indicate balanced performance across classes, with precision and recall closely aligned, suggesting that the classifier effectively identifies spam while maintaining low false positives on legitimate messages. The confusion matrix further confirms that misclassifications are minimal, consistent with expectations for TF–IDF paired with a regularized linear classifier on short-text data [@Shyrokykh2023ShortText].

Confusion matrix:

![Confusion Matrix](c:/Users/Admin/D803 QLN1 Task 2 Developing and Evaluating the Natural Language Processing Model/reports/confusion_matrix.png)

## F. Optimization Summary

To improve generalization, we performed a GridSearchCV over TF–IDF and Logistic Regression settings, varying the n-gram range, minimum document frequency, and the inverse regularization strength C [@Shyrokykh2023ShortText]. Five-fold cross-validation guided selection using weighted accuracy. The best configuration included bigrams (1–2), `min_df=3`, and `C=4.0`, yielding a best cross-validated score of 0.9805 (see `reports/best_params.json`).

These choices reflect common trade-offs in short-text pipelines: adding bigrams captures local phrase patterns that single tokens miss, while a slightly stronger regularization (higher C) balanced bias and variance for this sparse feature space [@MDPI2024TextClassificationReview]. Increasing `min_df` removed low-frequency noise terms that can hurt generalization. Additional avenues—such as LinearSVC or MultinomialNB baselines, lemmatization, and character n-grams—could be explored in future iterations if further improvements are needed [@MDPI2024TextClassificationReview].

## G. APA-Style Sources

Citations supporting CPU‑efficient, classical text classification with TF–IDF and Logistic Regression, plus recent reviews:

- Shyrokykh, K., Girnyk, M., & Dellmuth, L. M. (2023). Short text classification with machine learning in the social sciences: The case of climate change on Twitter. PLOS ONE, 18(9), e0290762. https://doi.org/10.1371/journal.pone.0290762
- Xiao, L., Li, Q., Ma, Q., Shen, J., Yang, Y., & Li, D. (2024). Text classification algorithm of tourist attractions subcategories with modified TF–IDF and Word2Vec. PLOS ONE, 19(10), e0305095. https://doi.org/10.1371/journal.pone.0305095
- Patuelli, R., Dugnani, L., Lanzilao, V., & Zambonelli, F. (2024). Text Classification: How Machine Learning Is Driving Performance and What’s Next. Information, 16(2), 130. https://doi.org/10.3390/info16020130
- Alsaeedi, A., Zubair, R., Khan, M., & Thayananthan, V. (2022). A systematic literature review on spam content detection and classification. Applied Sciences, 12(3), 1281. https://doi.org/10.3390/app12031281

Formatting notes:
- Use APA 7th edition in-text citations and references.
- If using Pandoc for references, the provided `docs/references.bib` works with:
  ```powershell
  pandoc "docs/assignment_writeup.md" --citeproc --csl=apa.csl --bibliography="docs/references.bib" -o "docs/assignment_writeup.docx"
  ```

## H. Professional Communication

- Document is organized, concise, and uses professional tone.
- Run Grammarly (as required) and fix flagged issues prior to submission.

---

## Reproducibility

1. Create and activate a virtual environment (optional):
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -U pip
   pip install -r requirements.txt
   ```
2. Train baseline and generate artifacts:
   ```powershell
   py -3 "src/train_baseline.py"
   ```
3. Run hyperparameter search:
   ```powershell
   py -3 "src/train_optimize.py"
   ```

## Convert this Markdown to DOCX with Pandoc

- Basic conversion:
  ```powershell
  pandoc "docs/assignment_writeup.md" -o "docs/assignment_writeup.docx"
  ```
- With citations (optional):
  ```powershell
  pandoc "docs/assignment_writeup.md" \
    --citeproc --csl=apa.csl --bibliography="docs/references.bib" \
    -o "docs/assignment_writeup.docx"
  ```

## GitLab Submission Checklist (A & B)

- Create subgroup and project in GitLab; clone to IDE.
- Commit and push after each step (B–G) with clear messages.
- Include repo URL in submission comments.
- Export branch history with commit messages and dates for submission.

Example (run in repo after you initialize git and push):
```powershell
git log --pretty=format:"%h | %ad | %s" --date=short > docs/branch_history.txt
```