# import streamlit as st
# from datetime import datetime

# from src.db.database import (
#     insert_entry,
#     assign_theme_for_latest,
#     fetch_entries,
#     fetch_entry_by_id,
#     delete_entry,
# )
# from src.prompts.prompt_engine import generate_prompts


# MOOD_MAP = {
#     "Struggling": 1,
#     "Low": 2,
#     "Neutral": 3,
#     "Good": 4,
#     "Great": 5,
# }


# def render_write_page():
#     # Load recent entries for prompt context + daily count
#     entries = fetch_entries(limit=50)

#     # -----------------------------
#     # Daily engagement nudge
#     # -----------------------------
#     today = datetime.now().date()
#     entries_today = 0
#     if not entries.empty:
#         entries_today = int((entries["created_at"].dt.date == today).sum())

#     if entries_today == 0:
#         st.caption("🌱 No entry yet today — even a few sentences counts.")
#     elif entries_today == 1:
#         st.caption("✨ You’ve checked in today. Want to add anything else?")
#     else:
#         st.caption(f"🔥 {entries_today} entries today — great consistency.")

#     # -----------------------------
#     # If user clicked an entry in sidebar, show it here (VIEW MODE)
#     # -----------------------------
#     selected_id = st.session_state.get("selected_entry_id")
#     if selected_id:
#         entry = fetch_entry_by_id(int(selected_id))

#         if entry is None:
#             st.warning("That entry no longer exists.")
#             st.session_state.selected_entry_id = None
#             st.rerun()

#         st.markdown("<div class='section-title'>Opened Entry</div>", unsafe_allow_html=True)
#         st.markdown(f"**{entry['created_at'].strftime('%A, %b %d • %I:%M %p')}**")
#         st.write(entry["text"])
#         st.caption(f"Mood: {entry.get('mood', 3)} / 5 • Sentiment: {float(entry.get('sentiment', 0)):+.2f}")

#         c1, c2 = st.columns([0.82, 0.18])
#         with c1:
#             if st.button("Close Entry"):
#                 st.session_state.selected_entry_id = None
#                 st.rerun()
#         with c2:
#             if st.button("Delete", help="Delete this entry permanently"):
#                 delete_entry(int(selected_id))
#                 st.session_state.selected_entry_id = None
#                 st.success("Entry deleted.")
#                 st.rerun()

#         st.markdown("---")

#     # -----------------------------
#     # WRITE MODE
#     # -----------------------------
#     st.markdown(
#         f"<div class='lumina-subtle'>{datetime.now().strftime('%A, %B %d').upper()}</div>",
#         unsafe_allow_html=True
#     )
#     st.markdown("<div class='lumina-h1'>What's on your mind today?</div>", unsafe_allow_html=True)

#     # Prompt card with refresh/dismiss
#     if "prompt_idx" not in st.session_state:
#         st.session_state.prompt_idx = 0
#     if "prompt_dismissed" not in st.session_state:
#         st.session_state.prompt_dismissed = False

#     prompts = generate_prompts(entries)
#     if not prompts:
#         prompts = ["What’s on your mind today?"]

#     current_prompt = prompts[st.session_state.prompt_idx % len(prompts)]

#     if not st.session_state.prompt_dismissed:
#         c1, c2 = st.columns([0.88, 0.12])
#         with c1:
#             st.markdown(
#                 f"""
#                 <div class="prompt-card">
#                   <div>
#                     <div class="prompt-title">TODAY'S PROMPT</div>
#                     <div class="prompt-text">{current_prompt}</div>
#                     <div style="margin-top:8px;color:#6b7280;font-size:12px;">
#                       Adapts based on themes and tone from your recent entries.
#                     </div>
#                   </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
#         with c2:
#             if st.button("↻", help="New prompt"):
#                 st.session_state.prompt_idx += 1
#                 st.session_state.prompt_dismissed = False
#                 st.rerun()
#             if st.button("✕", help="Dismiss"):
#                 st.session_state.prompt_dismissed = True
#                 st.rerun()

#     st.markdown("<div class='section-title'>How are you feeling?</div>", unsafe_allow_html=True)
#     mood_label = st.radio("", list(MOOD_MAP.keys()), horizontal=True, index=2)
#     if "journal_text" not in st.session_state:
#         st.session_state.journal_text = ""


#     text = st.text_area(
#     "",
#     placeholder="Start writing your thoughts...",
#     height=260,
#     key="journal_text"
# )

#     st.caption(f"{len((text or '').split())} words")

#     c3, c4 = st.columns([0.72, 0.28])
#     with c3:
#         st.caption("🔒 Your entries are private and stored locally.")
#     with c4:
#         if st.button("Save Entry", use_container_width=True):
#             if len((text or "").strip()) < 3:
#                 st.warning("Write a little more (even 1–2 sentences is fine).")
#             else:
#                 try:
#                     insert_entry(text, mood=MOOD_MAP[mood_label])
#                     assign_theme_for_latest()
#                     st.success("Saved.")
#                     st.session_state.journal_text = ""

#                     st.rerun()
#                 except Exception as e:
#                     st.error("Something went wrong saving your entry.")
#                     st.exception(e)
import streamlit as st
from datetime import datetime

from src.db.database import (
    insert_entry,
    assign_theme_for_latest,
    fetch_entries,
    fetch_entry_by_id,
    delete_entry,
)
from src.prompts.prompt_engine import generate_prompts


MOOD_MAP = {
    "Struggling": 1,
    "Low": 2,
    "Neutral": 3,
    "Good": 4,
    "Great": 5,
}


def _save_entry():
    """
    Streamlit-safe save callback.
    Reads from session_state, writes to DB, clears text box, then sets feedback flags.
    """
    text = (st.session_state.get("journal_text") or "").strip()
    mood_label = st.session_state.get("mood_label", "Neutral")
    mood_value = MOOD_MAP.get(mood_label, 3)

    if len(text) < 3:
        st.session_state["save_success"] = False
        st.session_state["save_error"] = "Write a little more (even 1–2 sentences is fine)."
        return

    try:
        insert_entry(text, mood=mood_value)
        assign_theme_for_latest()

        # ✅ clear inputs safely
        st.session_state["journal_text"] = ""
        st.session_state["mood_label"] = "Neutral"

        st.session_state["save_success"] = True
        st.session_state["save_error"] = None

    except Exception as e:
        st.session_state["save_success"] = False
        st.session_state["save_error"] = f"Save failed: {e}"

    st.session_state["prompt_idx"] += 1
    st.session_state["prompt_dismissed"] = False



def render_write_page():
    # init state defaults
    st.session_state.setdefault("prompt_idx", 0)
    st.session_state.setdefault("prompt_dismissed", False)
    st.session_state.setdefault("journal_text", "")
    st.session_state.setdefault("mood_label", "Neutral")
    st.session_state.setdefault("save_success", None)
    st.session_state.setdefault("save_error", None)

    # Load entries (for prompts + counts)
    entries = fetch_entries(limit=50)

    # -----------------------------
    # Daily engagement nudge
    # -----------------------------
    today = datetime.now().date()
    entries_today = 0
    if not entries.empty:
        entries_today = int((entries["created_at"].dt.date == today).sum())

    if entries_today == 0:
        st.caption("🌱 No entry yet today — even a few sentences counts.")
    elif entries_today == 1:
        st.caption("✨ You’ve checked in today. Want to add anything else?")
    else:
        st.caption(f"🔥 {entries_today} entries today — great consistency.")

    # -----------------------------
    # VIEW MODE: opened entry from sidebar
    # -----------------------------
    selected_id = st.session_state.get("selected_entry_id")
    if selected_id:
        entry = fetch_entry_by_id(int(selected_id))

        if entry is None:
            st.warning("That entry no longer exists.")
            st.session_state.selected_entry_id = None
            st.rerun()

        st.markdown("<div class='section-title'>Opened Entry</div>", unsafe_allow_html=True)
        st.markdown(f"**{entry['created_at'].strftime('%A, %b %d • %I:%M %p')}**")
        st.write(entry["text"])
        st.caption(
            f"Mood: {entry.get('mood', 3)} / 5 • Sentiment: {float(entry.get('sentiment', 0)):+.2f}"
        )

        c1, c2 = st.columns([0.82, 0.18])
        with c1:
            if st.button("Close Entry"):
                st.session_state.selected_entry_id = None
                st.rerun()
        with c2:
            if st.button("Delete", help="Delete this entry permanently"):
                delete_entry(int(selected_id))
                st.session_state.selected_entry_id = None
                st.success("Entry deleted.")
                st.rerun()

        st.markdown("---")

    # -----------------------------
    # WRITE MODE UI
    # -----------------------------
    st.markdown(
        f"<div class='lumina-subtle'>{datetime.now().strftime('%A, %B %d').upper()}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='lumina-h1'>What's on your mind today?</div>", unsafe_allow_html=True)

    # Feedback messages from last save
    if st.session_state.get("save_success") is True:
        st.success("Saved.")
        st.session_state["save_success"] = None  # consume message
    if st.session_state.get("save_error"):
        st.warning(st.session_state["save_error"])
        st.session_state["save_error"] = None  # consume message

    # Prompts
    prompts = generate_prompts(entries)
    if not prompts:
        prompts = ["What’s on your mind today?"]
    current_prompt = prompts[st.session_state.prompt_idx % len(prompts)]

    if not st.session_state.prompt_dismissed:
        c1, c2 = st.columns([0.88, 0.12])
        with c1:
            st.markdown(
                f"""
                <div class="prompt-card">
                  <div>
                    <div class="prompt-title">TODAY'S PROMPT</div>
                    <div class="prompt-text">{current_prompt}</div>
                    <div style="margin-top:8px;color:#6b7280;font-size:12px;">
                      Adapts based on themes and tone from your recent entries.
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            if st.button("↻", help="New prompt"):
                st.session_state.prompt_idx += 1
                st.session_state.prompt_dismissed = False
                st.rerun()
            if st.button("✕", help="Dismiss"):
                st.session_state.prompt_dismissed = True
                st.rerun()

    # Mood selector (with a key so we can reset it)
    st.markdown("<div class='section-title'>How are you feeling?</div>", unsafe_allow_html=True)
    st.radio("", list(MOOD_MAP.keys()), horizontal=True, key="mood_label", index=2)

    # Journal text (with a key so we can clear it)
    st.text_area(
        "",
        placeholder="Start writing your thoughts...",
        height=260,
        key="journal_text",
    )

    st.caption(f"{len((st.session_state.get('journal_text') or '').split())} words")

    c3, c4 = st.columns([0.72, 0.28])
    with c3:
        st.caption("🔒 Your entries are private and stored locally.")
    with c4:
        st.button("Save Entry", use_container_width=True, on_click=_save_entry)
