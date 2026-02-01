import streamlit as st

def inject_css():
    st.markdown("""
    <style>
      /* Layout spacing */
      .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

      /* Page titles */
      .lumina-h1 { font-size: 52px; font-weight: 600; margin: 0.4rem 0 0.8rem 0; }
      .lumina-subtle { color: #6b7280; font-size: 14px; }

      /* Prompt card */
      .prompt-card {
        border: 1px solid #e5e7eb;
        background: #f8fbff;
        border-radius: 14px;
        padding: 18px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
      }
      .prompt-title { font-size: 12px; letter-spacing: 0.12em; color: #2563eb; font-weight: 700; }
      .prompt-text { font-size: 18px; font-weight: 600; margin-top: 6px; }

      /* Chips */
      .chip-row { display: flex; gap: 10px; flex-wrap: wrap; }
      .chip {
        border: 1px solid #e5e7eb;
        border-radius: 999px;
        padding: 8px 14px;
        font-size: 14px;
        background: white;
      }

      /* Section header */
      .section-title { font-size: 18px; font-weight: 700; margin: 14px 0 10px 0; }

      /* Metric cards */
      .card {
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 16px;
        background: white;
      }
      .card-label { color:#6b7280; font-size: 14px; }
      .card-value { font-size: 34px; font-weight: 700; margin-top: 6px; }
    </style>
    """, unsafe_allow_html=True)
