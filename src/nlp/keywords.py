from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text: str, top_k: int = 6):
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform([text])
    terms = vec.get_feature_names_out()
    scores = X.toarray()[0]
    ranked = sorted(zip(terms, scores), key=lambda x: -x[1])
    return [term for term, _ in ranked[:top_k]]
