import argparse
import os
import re
import json
import pandas as pd
from typing import List

# NLP imports
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as SPACY_STOPWORDS

# Optional: NLTK stopwords fallback (only used if available)
try:
    import nltk
    from nltk.corpus import stopwords as nltk_stopwords
    nltk_available = True
except Exception:
    nltk_available = False

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
import joblib

# -----------------------------
# Helpers
# -----------------------------
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
MULTISPACE_RE = re.compile(r"\s+")
NON_ASCII_RE = re.compile(r"[^\x00-\x7F]+")


def map_score_to_label(score: int) -> str:
    if score >= 4:
        return "positive"
    if score <= 2:
        return "negative"
    return "neutral"


def basic_clean(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = URL_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = NON_ASCII_RE.sub(" ", text)
    text = text.lower()
    text = MULTISPACE_RE.sub(" ", text)
    return text.strip()


def spacy_process(nlp, text: str, stopword_set: set) -> dict:
    doc = nlp(text)
    # Keep alpha tokens only, remove stopwords and punctuation, keep length>1
    tokens: List[str] = [t.text for t in doc if t.is_alpha and not t.is_stop and t.text.lower() not in stopword_set and len(t.text) > 1]
    lemmas: List[str] = [t.lemma_ for t in doc if t.is_alpha and not t.is_stop and t.lemma_.lower() not in stopword_set and len(t.lemma_) > 1]
    cleaned_text = " ".join(tokens)
    return {"tokens": tokens, "lemmas": lemmas, "cleaned_text": cleaned_text}


def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)


def build_stopwords() -> set:
    s = set(w.lower() for w in SPACY_STOPWORDS)
    if nltk_available:
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            try:
                nltk.download('stopwords', quiet=True)
            except Exception:
                pass
        try:
            s.update(word.lower() for word in nltk_stopwords.words('english'))
        except Exception:
            pass
    return s


def main():
    parser = argparse.ArgumentParser(description="Preprocess Amazon Fine Food Reviews for sentiment analysis")
    parser.add_argument('--input', type=str, default=os.path.join('data', 'raw', 'Reviews.csv'), help='Path to Kaggle Amazon Reviews.csv')
    parser.add_argument('--sample_size', type=int, default=1000, help='Number of rows to sample (>=500)')
    parser.add_argument('--random_state', type=int, default=42)
    parser.add_argument('--save_raw', type=str, default=os.path.join('data', 'raw', 'amazon_sample.csv'))
    parser.add_argument('--save_processed', type=str, default=os.path.join('data', 'processed', 'amazon_processed.csv'))
    parser.add_argument('--tfidf', action='store_true', help='Also compute and save TF-IDF features')
    parser.add_argument('--tfidf_min_df', type=int, default=3)
    parser.add_argument('--tfidf_max_features', type=int, default=20000)
    parser.add_argument('--tfidf_out', type=str, default=os.path.join('data', 'processed', 'tfidf_features.npz'))
    parser.add_argument('--tfidf_vectorizer', type=str, default=os.path.join('data', 'processed', 'tfidf_vectorizer.pkl'))
    args = parser.parse_args()

    if args.sample_size < 500:
        raise ValueError("sample_size must be at least 500 to meet rubric requirements")

    # Paths
    raw_dir = os.path.join('data', 'raw')
    processed_dir = os.path.join('data', 'processed')
    ensure_dirs(raw_dir, processed_dir)

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}\nPlease download 'Amazon Fine Food Reviews' from Kaggle and place Reviews.csv at this path.")

    # Load
    df = pd.read_csv(args.input)
    # Expect columns: Id, Text, Score (Kaggle dataset)
    required_cols = {'Id', 'Text', 'Score'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Input CSV missing required columns: {missing}")

    # Drop missing text
    df = df.dropna(subset=['Text', 'Score']).copy()

    # Sample
    if len(df) > args.sample_size:
        df_sample = df.sample(n=args.sample_size, random_state=args.random_state)
    else:
        df_sample = df

    # Label mapping
    df_sample['label'] = df_sample['Score'].apply(map_score_to_label)

    # Save sampled raw
    df_sample[['Id', 'Text', 'Score', 'label']].to_csv(args.save_raw, index=False)

    # NLP Pipeline
    try:
        nlp = spacy.load('en_core_web_sm', disable=['ner'])
    except OSError:
        raise OSError("SpaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")

    stopword_set = build_stopwords()

    processed_records = []
    for _, row in df_sample.iterrows():
        rid = row['Id']
        text = str(row['Text'])
        label = row['label']
        cleaned = basic_clean(text)
        proc = spacy_process(nlp, cleaned, stopword_set)
        processed_records.append({
            'id': rid,
            'original_text': text,
            'cleaned_text': proc['cleaned_text'],
            'tokens': json.dumps(proc['tokens'], ensure_ascii=False),
            'lemmas': json.dumps(proc['lemmas'], ensure_ascii=False),
            'label': label
        })

    df_out = pd.DataFrame(processed_records)
    df_out.to_csv(args.save_processed, index=False)

    if args.tfidf:
        # Use cleaned_text for features
        texts = df_out['cleaned_text'].fillna("").tolist()
        vectorizer = TfidfVectorizer(min_df=args.tfidf_min_df, max_features=args.tfidf_max_features)
        X = vectorizer.fit_transform(texts)
        sparse.save_npz(args.tfidf_out, X)
        joblib.dump(vectorizer, args.tfidf_vectorizer)
        print(f"Saved TF-IDF features to {args.tfidf_out} and vectorizer to {args.tfidf_vectorizer}")

    print(f"Saved sampled raw to {args.save_raw}")
    print(f"Saved processed to {args.save_processed}")


if __name__ == '__main__':
    main()