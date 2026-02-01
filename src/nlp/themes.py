import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.config import THEME_SIM_THRESHOLD

def assign_theme(entry, conn):
    cur = conn.cursor()
    cur.execute("SELECT id, name, centroid FROM themes")
    themes = cur.fetchall()

    entry_text = entry["text"]

    if not themes:
        cur.execute(
            "INSERT INTO themes VALUES (NULL, ?, ?)",
            ("General", json.dumps(entry["keywords"]))
        )
        theme_id = cur.lastrowid
        cur.execute(
            "INSERT INTO entry_theme VALUES (?, ?, ?)",
            (entry["id"], theme_id, 1.0)
        )
        return

    docs = [json.loads(t[2]) for t in themes]
    docs = [" ".join(d) for d in docs] + [entry_text]

    vec = TfidfVectorizer()
    X = vec.fit_transform(docs)
    sims = cosine_similarity(X[-1], X[:-1])[0]

    best = sims.argmax()
    if sims[best] >= THEME_SIM_THRESHOLD:
        cur.execute(
            "INSERT INTO entry_theme VALUES (?, ?, ?)",
            (entry["id"], themes[best][0], float(sims[best]))
        )
    else:
        cur.execute(
            "INSERT INTO themes VALUES (NULL, ?, ?)",
            ("New Theme", json.dumps(entry["keywords"]))
        )
        new_id = cur.lastrowid
        cur.execute(
            "INSERT INTO entry_theme VALUES (?, ?, ?)",
            (entry["id"], new_id, 1.0)
        )
