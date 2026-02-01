import sqlite3
import json
from datetime import datetime, timedelta
import pandas as pd

from src.config import DB_PATH
from src.nlp.sentiment import sentiment_score
from src.nlp.keywords import extract_keywords
from src.nlp.themes import assign_theme

def connect():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        text TEXT,
        mood INTEGER,          -- NEW: 1..5 from pills
        sentiment REAL,
        keywords TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS themes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        centroid TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS entry_theme (
        entry_id INTEGER,
        theme_id INTEGER,
        strength REAL
    )""")

    conn.commit()
    conn.close()

def insert_entry(text: str, mood: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO entries VALUES (NULL, ?, ?, ?, ?, ?)",
        (
            datetime.now().isoformat(),
            text,
            int(mood),
            float(sentiment_score(text)),
            json.dumps(extract_keywords(text))
        )
    )
    conn.commit()
    conn.close()

def fetch_entries(limit: int = 500) -> pd.DataFrame:
    conn = connect()
    df = pd.read_sql("SELECT * FROM entries ORDER BY created_at DESC LIMIT ?", conn, params=(limit,))
    conn.close()
    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["keywords"] = df["keywords"].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
    return df

def assign_theme_for_latest():
    conn = connect()
    df = pd.read_sql("SELECT * FROM entries ORDER BY id DESC LIMIT 1", conn)
    if df.empty:
        conn.close()
        return
    entry = df.iloc[0]
    assign_theme(entry, conn)
    conn.commit()
    conn.close()

def delete_all_data():
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM entry_theme")
    cur.execute("DELETE FROM entries")
    cur.execute("DELETE FROM themes")
    conn.commit()
    conn.close()

def fetch_entries_grouped_for_sidebar(limit=20):
    """
    Returns labels like Today / Yesterday / Jan 29 with counts.
    """
    conn = connect()
    df = pd.read_sql("SELECT created_at FROM entries ORDER BY created_at DESC LIMIT ?", conn, params=(limit,))
    conn.close()

    if df.empty:
        return []

    df["created_at"] = pd.to_datetime(df["created_at"])
    today = datetime.now().date()
    yday = today - timedelta(days=1)

    def label(d):
        dd = d.date()
        if dd == today: return "Today"
        if dd == yday: return "Yesterday"
        return d.strftime("%b %d")

    df["label"] = df["created_at"].apply(label)
    groups = df.groupby("label").size().reset_index(name="count")
    # keep display order as they appear in df
    order = []
    for x in df["label"]:
        if x not in order:
            order.append(x)
    groups["order"] = groups["label"].apply(lambda x: order.index(x))
    groups = groups.sort_values("order")
    return list(zip(groups["label"], groups["count"]))
def fetch_entry_summaries(limit: int = 50):
    """
    Lightweight list for sidebar: id, created_at, mood, sentiment, preview
    """
    conn = connect()
    df = pd.read_sql(
        "SELECT id, created_at, text, mood, sentiment FROM entries ORDER BY created_at DESC LIMIT ?",
        conn,
        params=(limit,)
    )
    conn.close()

    if df.empty:
        return df

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["preview"] = df["text"].fillna("").apply(lambda s: (s[:60] + "…") if len(s) > 60 else s)
    return df[["id", "created_at", "mood", "sentiment", "preview"]]


def fetch_entry_by_id(entry_id: int):
    conn = connect()
    df = pd.read_sql("SELECT * FROM entries WHERE id = ?", conn, params=(entry_id,))
    conn.close()
    if df.empty:
        return None
    row = df.iloc[0].to_dict()
    row["created_at"] = pd.to_datetime(row["created_at"])
    row["keywords"] = json.loads(row["keywords"]) if isinstance(row.get("keywords"), str) else []
    if "mood" not in row or row["mood"] is None:
        row["mood"] = 3
    return row


def delete_entry(entry_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM entry_theme WHERE entry_id = ?", (entry_id,))
    cur.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
