# import streamlit as st
# from datetime import datetime, timedelta

# from src.db.database import fetch_entry_summaries, delete_all_data


# def render_sidebar() -> str:
#     with st.sidebar:
#         st.markdown("## ✨ Echo")
#         st.markdown(
#     """
#     <div style="
#         background:#f8fafc;
#         border:1px solid #e5e7eb;
#         padding:12px 12px;
#         border-radius:12px;
#         margin-top:8px;
#         margin-bottom:14px;
#         ">
#       <div style="font-size:12px; letter-spacing:0.08em; color:#64748b; font-weight:600;">
#         ABOUT
#       </div>
#       <div style="font-size:14px; color:#111827; margin-top:6px; line-height:1.35;">
#         Echo is a private journaling companion that helps you reflect daily with gentle prompts,
#         mood tracking, and local insights — your entries stay on your device.
#       </div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )



#         # -----------------------------
#         # Navigation (no radio buttons)
#         # -----------------------------
#         st.markdown("### NAVIGATION")

#         if "page" not in st.session_state:
#             st.session_state.page = "Write"

#         def nav_button(label, icon, page_name):
#             is_active = st.session_state.page == page_name

#             clicked = st.button(
#                 f"{icon} {label}",
#                 key=f"nav_{page_name}",
#                 use_container_width=True,
#             )

#             # Active highlight (simple + clean)
#             if is_active:
#                 st.markdown(
#                     "<div style='height:6px;background:#e6f0ff;border-left:4px solid #2563eb;"
#                     "border-radius:6px;margin-top:-6px;margin-bottom:10px;'></div>",
#                     unsafe_allow_html=True,
#                 )
#             else:
#                 st.markdown("<div style='height:6px;margin-bottom:10px;'></div>", unsafe_allow_html=True)

#             if clicked:
#                 st.session_state.page = page_name
#                 st.session_state.selected_entry_id = None
#                 st.rerun()

#         nav_button("Write", "✏️", "Write")
#         nav_button("Insights", "📊", "Insights")
#         nav_button("Reflections", "🧠", "Reflections")

#         page = st.session_state.page

#         st.markdown("---")

#         # -----------------------------
#         # Recent Entries (grouped)
#         # -----------------------------
#         st.markdown("### RECENT ENTRIES")

#         df = fetch_entry_summaries(limit=60)

#         if df.empty:
#             st.caption("No entries yet.")
#         else:
#             today = datetime.now().date()
#             yesterday = today - timedelta(days=1)

#             def group_label(dt):
#                 d = dt.date()
#                 if d == today:
#                     return "Today"
#                 if d == yesterday:
#                     return "Yesterday"
#                 return dt.strftime("%b %d")

#             df["group"] = df["created_at"].apply(group_label)

#             # Keep groups in first-seen order
#             seen = set()
#             ordered_groups = []
#             for g in df["group"].tolist():
#                 if g not in seen:
#                     seen.add(g)
#                     ordered_groups.append(g)

#             for g in ordered_groups:
#                 group_df = df[df["group"] == g]

#                 with st.expander(f"{g} ({len(group_df)})", expanded=(g == "Today")):
#                     for _, row in group_df.iterrows():
#                         label = f"{row['created_at'].strftime('%I:%M %p')} • {row['preview']}"
#                         if st.button(label, key=f"open_{row['id']}"):
#                             st.session_state.selected_entry_id = int(row["id"])
#                             st.session_state.page = "Write"
#                             st.rerun()

#         st.markdown("---")

#         # -----------------------------
#         # Data Controls
#         # -----------------------------
#         st.markdown("### DATA")

#         if "confirm_clear" not in st.session_state:
#             st.session_state.confirm_clear = False

#         if st.button("🗑️ Clear all entries"):
#             st.session_state.confirm_clear = True

#         if st.session_state.confirm_clear:
#             st.warning("This will permanently delete all entries.")
#             c1, c2 = st.columns(2)
#             with c1:
#                 if st.button("Yes, delete"):
#                     delete_all_data()
#                     st.session_state.confirm_clear = False
#                     st.session_state.selected_entry_id = None
#                     st.success("Deleted.")
#                     st.rerun()
#             with c2:
#                 if st.button("Cancel"):
#                     st.session_state.confirm_clear = False

#         st.caption("🔒 Your data stays on this device.")

#     return page
import streamlit as st
from datetime import datetime, timedelta

from src.db.database import fetch_entry_summaries, delete_all_data


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## ✨ Echo")

        # -----------------------------
        # Navigation (ALL inside sidebar)
        # -----------------------------
        st.markdown("### NAVIGATION")

        if "page" not in st.session_state:
            st.session_state.page = "Write"

        def nav_button(label, icon, page_name):
            is_active = st.session_state.page == page_name

            clicked = st.button(
                f"{icon} {label}",
                key=f"nav_{page_name}",
                use_container_width=True,
            )

            # Active highlight (simple)
            if is_active:
                st.markdown(
                    "<div style='height:6px;background:#e6f0ff;border-left:4px solid #2563eb;"
                    "border-radius:6px;margin-top:-6px;margin-bottom:10px;'></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<div style='height:6px;margin-bottom:10px;'></div>", unsafe_allow_html=True)

            if clicked:
                st.session_state.page = page_name
                st.session_state.selected_entry_id = None
                st.rerun()

        # ✅ These buttons are now in sidebar
        nav_button("Write", "✏️", "Write")
        nav_button("Insights", "📊", "Insights")
        nav_button("Reflections", "🧠", "Reflections")
        nav_button("About", "ℹ️", "About")

        page = st.session_state.page

        st.markdown("---")

        # -----------------------------
        # Recent Entries
        # -----------------------------
        st.markdown("### RECENT ENTRIES")

        df = fetch_entry_summaries(limit=60)

        if df.empty:
            st.caption("No entries yet.")
        else:
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)

            def group_label(dt):
                d = dt.date()
                if d == today:
                    return "Today"
                if d == yesterday:
                    return "Yesterday"
                return dt.strftime("%b %d")

            df["group"] = df["created_at"].apply(group_label)

            seen = set()
            ordered_groups = []
            for g in df["group"].tolist():
                if g not in seen:
                    seen.add(g)
                    ordered_groups.append(g)

            for g in ordered_groups:
                group_df = df[df["group"] == g]

                with st.expander(f"{g} ({len(group_df)})", expanded=(g == "Today")):
                    for _, row in group_df.iterrows():
                        label = f"{row['created_at'].strftime('%I:%M %p')} • {row['preview']}"
                        if st.button(label, key=f"open_{row['id']}"):
                            st.session_state.selected_entry_id = int(row["id"])
                            st.session_state.page = "Write"
                            st.rerun()

        st.markdown("---")

        # -----------------------------
        # Data controls
        # -----------------------------
        st.markdown("### DATA")

        if "confirm_clear" not in st.session_state:
            st.session_state.confirm_clear = False

        if st.button("🗑️ Clear all entries"):
            st.session_state.confirm_clear = True

        if st.session_state.confirm_clear:
            st.warning("This will permanently delete all entries.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Yes, delete"):
                    delete_all_data()
                    st.session_state.confirm_clear = False
                    st.session_state.selected_entry_id = None
                    st.success("Deleted.")
                    st.rerun()
            with c2:
                if st.button("Cancel"):
                    st.session_state.confirm_clear = False

        st.caption("🔒 Your data stays on this device.")

    return page
