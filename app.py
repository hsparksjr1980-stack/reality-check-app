import streamlit as st
from app_state import initialize_app_state, reset_assessment_state
from buildout_tracker_ui import render_buildout_tracker
from nav_ui import render_page_nav
from page_config import DEFAULT_PAGE, PAGES
from phase_gate import guard_page_or_warn
from plans_support_ui import render_plans_support
from profile_ui import render_profile_setup
from shared_ui import render_brand_header, render_profile_strip
from theme import apply_theme
from welcome_ui import render_welcome
from overview_ui import render_overview
from final_decision_ui import render_final_decision
from post_discovery_ui import render_post_discovery
from deal_workspace_ui import render_deal_workspace
from deal_model_ui import render_deal_model
from financial_model_ui import render_financial_model
from phase0_ui import render_phase_0
from phase1_ui import render_phase_1
from opportunity_fit_ui import render_opportunity_fit


st.set_page_config(page_title="Reality Check", layout="wide")
apply_theme()
initialize_app_state()



def sync_page_from_sidebar() -> None:
    st.session_state["current_page"] = st.session_state["sidebar_page_selector"]


render_brand_header(
    "Reality Check",
    "A decision system for determining whether a franchise opportunity is worth pursuing, financing, and negotiating.",
)

if not st.session_state["auth_complete"]:
    render_welcome()
    st.stop()

if not st.session_state["profile_complete"]:
    render_profile_setup()
    st.stop()

st.sidebar.title("Reality Check")

if st.sidebar.button("Reset Assessment"):
    reset_assessment_state(
        keys_to_keep=[
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
    )
    st.session_state["current_page"] = DEFAULT_PAGE
    st.rerun()

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

if not guard_page_or_warn(page):
    render_page_nav(PAGES, page)
    st.stop()

if page == "Overview":
    render_overview()
elif page == "Reality Check":
    render_phase_0()
elif page == "Concept Validation":
    render_phase_1()
elif page == "Opportunity Fit & Recommendations":
    render_opportunity_fit()
elif page == "Financial Model":
    render_financial_model()
elif page == "Post-Discovery":
    render_post_discovery()
elif page == "Final Decision":
    render_final_decision()
elif page == "Plans & Support":
    render_plans_support()
elif page == "Deal Workspace":
    render_deal_workspace()
elif page == "Deal Model":
    render_deal_model()
elif page == "Buildout & Launch Tracker":
    render_buildout_tracker()

render_page_nav(PAGES, page)
