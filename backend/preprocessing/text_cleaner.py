import re
import nltk
import spacy

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt")
nltk.download("stopwords")

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):

    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        "",
        text
    )

    tokens = word_tokenize(text)

    stop_words = set(
        stopwords.words("english")
    )

    tokens = [
        word
        for word in tokens
        if word not in stop_words
    ]

    doc = nlp(" ".join(tokens))

    lemmas = [
        token.lemma_
        for token in doc
    ]

    return " ".join(lemmas)