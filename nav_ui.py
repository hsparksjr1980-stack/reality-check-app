import streamlit as st

def render_page_nav(pages, current_page):
    idx = pages.index(current_page)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if idx > 0:
            if st.button("← Back", key=f"back_{current_page}"):
                st.session_state["current_page"] = pages[idx - 1]
                st.rerun()

    with col3:
        if idx < len(pages) - 1:
            if st.button("Next →", key=f"next_{current_page}"):
                st.session_state["current_page"] = pages[idx + 1]
                st.rerun()
