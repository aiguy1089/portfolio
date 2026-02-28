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
    parser = argparse.ArgumentParser(description="Preprocess Amazon Books 500 Reviews for sentiment analysis")
    parser.add_argument('--input', type=str, default=os.path.join('amazon_books_500_reviews.csv'), help='Path to amazon_books_500_reviews.csv')
    parser.add_argument('--save_processed', type=str, default=os.path.join('data', 'processed', 'books_processed.csv'))
    parser.add_argument('--tfidf', action='store_true', help='Also compute and save TF-IDF features')
    parser.add_argument('--tfidf_min_df', type=int, default=2)
    parser.add_argument('--tfidf_max_features', type=int, default=10000)
    parser.add_argument('--tfidf_out', type=str, default=os.path.join('data', 'processed', 'books_tfidf_features.npz'))
    parser.add_argument('--tfidf_vectorizer', type=str, default=os.path.join('data', 'processed', 'books_tfidf_vectorizer.pkl'))
    args = parser.parse_args()

    processed_dir = os.path.join('data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}")

    # Load input with expected columns
    df = pd.read_csv(args.input)
    # Normalize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]
    required_cols = {'review_id', 'review_text', 'star_rating', 'sentiment'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Input CSV missing required columns: {missing}")

    # Ensure >=500 rows (already satisfied by file name, but we assert)
    if len(df) < 500:
        raise ValueError(f"Dataset must have at least 500 items; found {len(df)}")

    # Clean text and process
    try:
        nlp = spacy.load('en_core_web_sm', disable=['ner'])
    except OSError:
        raise OSError("SpaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")

    stopword_set = build_stopwords()

    records = []
    for _, row in df.iterrows():
        rid = row['review_id']
        text = str(row['review_text'])
        stars = int(row['star_rating'])
        label = str(row['sentiment']).strip().lower()
        cleaned = basic_clean(text)
        proc = spacy_process(nlp, cleaned, stopword_set)
        records.append({
            'id': rid,
            'original_text': text,
            'cleaned_text': proc['cleaned_text'],
            'tokens': json.dumps(proc['tokens'], ensure_ascii=False),
            'lemmas': json.dumps(proc['lemmas'], ensure_ascii=False),
            'star_rating': stars,
            'label': label
        })

    df_out = pd.DataFrame(records)
    df_out.to_csv(args.save_processed, index=False)

    if args.tfidf:
        texts = df_out['cleaned_text'].fillna("").tolist()
        vectorizer = TfidfVectorizer(min_df=args.tfidf_min_df, max_features=args.tfidf_max_features)
        X = vectorizer.fit_transform(texts)
        sparse.save_npz(args.tfidf_out, X)
        joblib.dump(vectorizer, args.tfidf_vectorizer)
        print(f"Saved TF-IDF features to {args.tfidf_out} and vectorizer to {args.tfidf_vectorizer}")

    print(f"Saved processed to {args.save_processed}")


if __name__ == '__main__':
    main()