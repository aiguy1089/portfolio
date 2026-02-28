from __future__ import annotations
import re
from typing import Iterable, List

import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk import download as nltk_download

# Ensure stopwords are available
try:
    stopwords.words("english")
except LookupError:
    nltk_download("stopwords")


def basic_clean(text: str, lowercase: bool = True, remove_punct: bool = True, remove_numbers: bool = False) -> str:
    if not isinstance(text, str):
        return ""
    t = text
    if lowercase:
        t = t.lower()
    if remove_numbers:
        t = re.sub(r"\d+", " ", t)
    if remove_punct:
        t = re.sub(r"[^a-zA-Z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def remove_stop_words(texts: Iterable[str]) -> List[str]:
    sw = set(stopwords.words("english"))
    out: List[str] = []
    for t in texts:
        tokens = [w for w in t.split() if w not in sw]
        out.append(" ".join(tokens))
    return out