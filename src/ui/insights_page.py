import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from src.db.database import fetch_entries

def render_insights_page():
    st.markdown("<div class='lumina-subtle'>YOUR JOURNEY</div>", unsafe_allow_html=True)
    st.markdown("<div class='lumina-h1'>Emotional Insights</div>", unsafe_allow_html=True)
    st.caption("Discover patterns in your thoughts and feelings")

    entries = fetch_entries(limit=500)
    if entries.empty:
        st.info("Add a few entries to unlock insights.")
        return

    # Metrics
    avg_mood = entries["mood"].mean()
    total_entries = len(entries)
    streak = _writing_streak(entries)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='card'><div class='card-label'>Average Mood</div><div class='card-value'>{avg_mood:.1f} <span style='font-size:16px;color:#6b7280'>/ 5</span></div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='card'><div class='card-label'>Total Entries</div><div class='card-value'>{total_entries}</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='card'><div class='card-label'>Writing Streak</div><div class='card-value'>{streak} <span style='font-size:16px;color:#6b7280'>days</span></div></div>", unsafe_allow_html=True)

    st.write("")
    st.subheader("Sentiment Distribution")

    pos = int((entries["sentiment"] > 0.15).sum())
    neu = int(((entries["sentiment"] >= -0.15) & (entries["sentiment"] <= 0.15)).sum())
    chal = int((entries["sentiment"] < -0.15).sum())
    total = max(1, len(entries))

    pos_pct = pos / total
    neu_pct = neu / total
    chal_pct = chal / total

    st.write(f"Positive **{pos_pct:.0%}** · Neutral **{neu_pct:.0%}** · Challenging **{chal_pct:.0%}**")

    def bar(label, pct, count, color):
        st.markdown(
            f"""
            <div style="margin:10px 0;">
            <div style="display:flex;justify-content:space-between;font-size:14px;">
                <span><b>{label}</b></span>
                <span style="color:#6b7280;">{count} entries</span>
            </div>
            <div style="background:#eef2f7;border-radius:999px;height:12px;overflow:hidden;">
                <div style="width:{pct*100:.1f}%;background:{color};height:12px;"></div>
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    bar("Positive", pos_pct, pos, "#2563eb")     # blue
    bar("Neutral", neu_pct, neu, "#9ca3af")      # gray
    bar("Challenging", chal_pct, chal, "#ef4444")# red
    st.write("")
    st.subheader("Patterns You Might Find Helpful")

    pattern = movement_mood_pattern(entries)
    if pattern:
        st.info(pattern)
    else:
        st.caption("Patterns will appear as you continue journaling.")


    # Simple theme labels from keywords (MVP): show top keywords across entries
    top_terms = _top_keywords(entries)
    chips = " ".join([f"<span class='chip'>{k} <span style='opacity:.6'>{v}</span></span>" for k, v in top_terms])
    st.markdown(f"<div class='chip-row'>{chips}</div>", unsafe_allow_html=True)

    st.write("")
    st.subheader("Mood Timeline")

    timeline = (
        entries.sort_values("created_at")
        .set_index("created_at")["mood"]
        .resample("D")
        .mean()
        .dropna()
        .tail(14)
    )

    fig = plt.figure()
    plt.bar(timeline.index.strftime("%a"), timeline.values)
    plt.ylim(1, 5)
    plt.ylabel("Mood (1–5)")
    st.pyplot(fig, clear_figure=True)

def _writing_streak(entries):
    dates = set(entries["created_at"].dt.date.tolist())
    streak = 0
    d = datetime.now().date()
    while d in dates:
        streak += 1
        d = d - timedelta(days=1)
    return streak

def _top_keywords(entries, top_n=10):
    counts = {}
    for kws in entries["keywords"]:
        for k in (kws or [])[:6]:
            counts[k] = counts.get(k, 0) + 1
    items = sorted(counts.items(), key=lambda x: -x[1])[:top_n]
    return items
def movement_mood_pattern(entries):
    """
    Detects whether entries mentioning movement correlate with higher mood.
    """
    movement_words = {"walk", "walking", "exercise", "gym", "run", "running", "yoga"}

    with_move = []
    without_move = []

    for _, row in entries.iterrows():
        kws = set((row.get("keywords") or []))
        if kws & movement_words:
            with_move.append(row["mood"])
        else:
            without_move.append(row["mood"])

    if len(with_move) >= 2 and len(without_move) >= 2:
        avg_with = sum(with_move) / len(with_move)
        avg_without = sum(without_move) / len(without_move)

        if avg_with >= avg_without + 0.4:
            return (
                "🧠 **Pattern noticed:** On days you mention movement (like walking or exercise), "
                "your mood tends to be higher. This may be a meaningful support habit for you."
            )

    return None
