import streamlit as st
from src.db.database import init_db
from src.ui.styles import inject_css
from src.ui.layout import render_sidebar
from src.ui.write_page import render_write_page
from src.ui.insights_page import render_insights_page
from src.ui.reflections_page import render_reflections_page
from src.ui.about_page import render_about_page


st.set_page_config(page_title="Echo (Local)", layout="wide")
init_db()
inject_css()

page = render_sidebar()

if page == "Write":
    render_write_page()
elif page == "Insights":
    render_insights_page()
elif page == "About":
    render_about_page()
else:
    render_reflections_page()
