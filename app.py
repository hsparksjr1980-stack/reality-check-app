import streamlit as st
from theme import apply_theme
from shared_ui import render_brand_header, render_profile_strip
from welcome_ui import render_welcome
from profile_ui import render_profile_setup
from overview_ui import render_overview
from final_decision_ui import render_final_decision
from post_discovery_ui import render_post_discovery
from deal_workspace_ui import render_deal_workspace
from deal_model_ui import render_deal_model

from phase0_ui import render_phase_0
from phase1_ui import render_phase_1
from nav_ui import render_page_nav

PAGES = [
    "Overview",
    "Reality Check",
    "Concept Validation",
    "Financial Model",
    "Post-Discovery Review",
    "Final Decision",
    "Deal Workspace (Pro)",
    "Deal Model (Pro)",
]

st.set_page_config(page_title="Reality Check", layout="wide")
apply_theme()

st.session_state.setdefault("auth_complete", False)
st.session_state.setdefault("profile_complete", False)
st.session_state.setdefault("current_page", "Overview")
st.session_state.setdefault("account_mode", None)
st.session_state.setdefault("premium_access", False)

def sync_page_from_sidebar():
    st.session_state["current_page"] = st.session_state["sidebar_page_selector"]

render_brand_header(
    "Reality Check",
    "A decision system for determining whether a franchise opportunity is worth pursuing, financing, and negotiating."
)

if not st.session_state["auth_complete"]:
    render_welcome()
    st.stop()

if not st.session_state["profile_complete"]:
    render_profile_setup()
    st.stop()

st.sidebar.title("Reality Check")

if st.sidebar.button("Reset Assessment"):
    keys_to_keep = [
        "auth_complete",
        "profile_complete",
        "full_name",
        "email",
        "city_state",
        "franchise_name",
        "units_considered",
        "ownership_style",
        "signed_anything",
        "premium_access",
    ]

    keys_to_delete = [k for k in list(st.session_state.keys()) if k not in keys_to_keep]

    for key in keys_to_delete:
        del st.session_state[key]

    st.session_state["current_page"] = "Overview"
    st.rerun()

if "sidebar_page_selector" not in st.session_state:
    st.session_state["sidebar_page_selector"] = st.session_state["current_page"]

if st.session_state["sidebar_page_selector"] != st.session_state["current_page"]:
    st.session_state["sidebar_page_selector"] = st.session_state["current_page"]

st.sidebar.radio(
    "Go to section:",
    PAGES,
    key="sidebar_page_selector",
    on_change=sync_page_from_sidebar,
)

page = st.session_state["current_page"]

render_profile_strip()
st.markdown("---")

if page == "Overview":
    render_overview()
    render_page_nav(PAGES, page)

elif page == "Reality Check":
    render_phase_0()
    render_page_nav(PAGES, page)

elif page == "Concept Validation":
    render_phase_1()
    render_page_nav(PAGES, page)

elif page == "Financial Model":
    st.header("Financial Model")
    st.write(
        "This section should pressure-test startup capital, debt, ramp assumptions, break-even, and cash fragility before you commit more serious effort."
    )
    st.info(
        "This is the point where you decide whether the opportunity is financially viable enough to justify deeper pursuit."
    )

    from pathlib import Path

    model_path = Path(__file__).parent / "financial_model_ui.py"
    if not model_path.exists():
        st.error(
            "financial_model_ui.py was not found in this folder. Add your existing model file here to complete the app."
        )
    else:
        code = model_path.read_text(encoding="utf-8")
        exec_globals = {"__name__": "__main__"}
        exec(code, exec_globals)

    render_page_nav(PAGES, page)

elif page == "Post-Discovery Review":
    render_post_discovery()
    render_page_nav(PAGES, page)

elif page == "Final Decision":
    render_final_decision()
    render_page_nav(PAGES, page)
    
elif page == "Deal Workspace (Pro)":
    render_deal_workspace()
    render_page_nav(PAGES, page)
    
elif page == "Deal Model (Pro)":
    render_deal_model()
    render_page_nav(PAGES, page)
    
