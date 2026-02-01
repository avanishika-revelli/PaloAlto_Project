import streamlit as st

def render_about_page():
    st.markdown("<div class='lumina-subtle'>ABOUT</div>", unsafe_allow_html=True)
    st.markdown("<div class='lumina-h1'>About Echo</div>", unsafe_allow_html=True)

    st.write("Echo is a private, empathetic journaling companion designed to make daily reflection easy.")

    st.markdown("### What Echo does")
    st.markdown(
        """
- **Dynamic prompts** that adapt based on your recent entries  
- **Mood check-ins** to track how you feel over time  
- **Local insights**: sentiment trends + recurring themes  
- **Weekly reflections** to connect the dots gently  
- **Full control**: view entries, delete entries, clear all data  
        """
    )

    st.markdown("### Privacy & trust")
    st.markdown(
        """
- Your journal is stored **locally on your device** (SQLite).
- No cloud sync by default.
- Designed to be **non-judgmental** and supportive.
        """
    )

    st.markdown("### Tech stack")
    st.markdown(
        """
- **Streamlit** UI  
- **SQLite** local storage  
- Lightweight **NLP**: keyword/theme extraction + sentiment scoring  
        """
    )
