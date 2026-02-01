import streamlit as st
from src.db.database import fetch_entries
from src.insights.weekly_reflection import weekly_reflection

def render_reflections_page():
    st.markdown("<div class='lumina-subtle'>REFLECTION TIME</div>", unsafe_allow_html=True)
    st.markdown("<div class='lumina-h1'>Your Weekly Reflections</div>", unsafe_allow_html=True)
    st.caption("AI-powered summaries to help you connect the dots")

    entries = fetch_entries(limit=500)
    if entries.empty:
        st.info("Write a few entries to generate reflections.")
        return

        # Weekly Reflections (only)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"<div class='card'><div class='card-label'>Entries Written</div>"
            f"<div class='card-value'>{len(entries.head(7))}</div></div>",
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"<div class='card'><div class='card-label'>Average Mood</div>"
            f"<div class='card-value'>{entries['mood'].mean():.1f}</div></div>",
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"<div class='card'><div class='card-label'>Themes Explored</div>"
            f"<div class='card-value'>{len(set(sum(entries['keywords'].tolist(), [])))}</div></div>",
            unsafe_allow_html=True
        )

    st.write("")
    st.subheader("AI-Generated Summary")
    st.write(weekly_reflection(entries))

    if st.button("Regenerate Insights"):
        st.rerun()

    st.write("")
    st.subheader("Suggested Next Steps")

    s1, s2 = st.columns(2)
    with s1:
        st.markdown(
            "<div class='card'><div class='card-value' style='font-size:18px'>Morning Journaling</div>"
            "<div class='card-label'>Try writing in the morning for a week</div></div>",
            unsafe_allow_html=True
        )
    with s2:
        st.markdown(
            "<div class='card'><div class='card-value' style='font-size:18px'>Gratitude Practice</div>"
            "<div class='card-label'>End each entry with three gratitudes</div></div>",
            unsafe_allow_html=True
        )
