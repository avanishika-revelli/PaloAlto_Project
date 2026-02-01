import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def render_dashboard(entries):
    st.subheader("📊 Trends")

    if entries is None or entries.empty:
        st.info("No data yet.")
        return

    df = entries.copy()
    df["created_at"] = pd.to_datetime(df["created_at"])
    df = df.sort_values("created_at")

    # ✅ group by day for a clean line (avoid weird spikes from multiple same-day entries)
    daily = (
        df.set_index("created_at")["sentiment"]
        .resample("D")
        .mean()
        .dropna()
        .tail(30)
    )

    fig = plt.figure()
    plt.plot(daily.index, daily.values, marker="o")
    plt.ylim(-1, 1)  # sentiment range
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Daily Avg Sentiment (-1 to +1)")
    plt.xlabel("Date")
    plt.grid(True, alpha=0.2)

    st.pyplot(fig, clear_figure=True)

    st.subheader("🗂️ Recent Entries")
    for row in df.tail(7).itertuples():
        with st.expander(row.created_at.strftime("%Y-%m-%d %H:%M")):
            st.write(row.text)
            st.caption(f"Sentiment: {row.sentiment:+.2f}")
