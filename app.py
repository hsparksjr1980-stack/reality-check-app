# app.py

from __future__ import annotations

from collections.abc import Callable
from typing import Final

import streamlit as st

from app_state import initialize_app_state, reset_assessment_state
from buildout_tracker_ui import render_buildout_tracker
from deal_model_ui import render_deal_model
from deal_workspace_ui import render_deal_workspace
from execution_report_ui import render_execution_report
from final_decision_ui import render_final_decision
from financial_model_ui import render_financial_model
from free_report_ui import render_free_report
from nav_ui import render_page_nav
from opportunity_fit_ui import render_opportunity_fit
from overview_ui import render_overview
from page_config import DEFAULT_PAGE, PAGES
from phase0_ui import render_phase_0
from phase1_ui import render_phase_1
from phase_gate import guard_page_or_warn
from plans_support_ui import render_plans_support
from post_discovery_ui import render_post_discovery
from profile_ui import render_profile_setup
from report_ui import render_report_screen
from shared_ui import render_brand_header, render_profile_strip
from theme import apply_theme
from ui_styles import inject_global_styles
from welcome_ui import render_welcome
from paywall_ui import render_paywall
from page_config import DEFAULT_PAGE, PAGES, SIDEBAR_PAGES


PageRenderer = Callable[[], None]

APP_TITLE: Final[str] = "Reality Check"
APP_DESCRIPTION: Final[str] = (
    "A decision system for determining whether a franchise opportunity is worth "
    "pursuing, financing, and negotiating."
)

RESET_KEYS_TO_KEEP: Final[list[str]] = [
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
    "dev_pro_access",
]

PAGE_RENDERERS: Final[dict[str, PageRenderer]] = {
    "Overview": render_overview,
    "Reality Check": render_phase_0,
    "Concept Validation": render_phase_1,
    "Opportunity Fit & Recommendations": render_opportunity_fit,
    "Financial Model": render_financial_model,
    "Free Report": render_free_report,
    "Post-Discovery": render_post_discovery,
    "Final Decision": render_final_decision,
    "Report": render_report_screen,
    "Plans & Support": render_plans_support,
    "Deal Workspace": render_deal_workspace,
    "Deal Model": render_deal_model,
    "Buildout & Launch Tracker": render_buildout_tracker,
    "Execution Report": render_execution_report,
    "Paywall": render_paywall,
}


def configure_app() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    apply_theme()
    initialize_app_state()
    inject_global_styles()


def ensure_required_state() -> None:
    st.session_state.setdefault("auth_complete", False)
    st.session_state.setdefault("profile_complete", False)
    st.session_state.setdefault("premium_access", False)
    st.session_state.setdefault("dev_pro_access", True)

    current_page = st.session_state.get("current_page", DEFAULT_PAGE)
    if current_page not in PAGES:
        current_page = DEFAULT_PAGE
    st.session_state["current_page"] = current_page


def render_app_header() -> None:
    render_brand_header(APP_TITLE, APP_DESCRIPTION)


def render_gates() -> bool:
    if not st.session_state["auth_complete"]:
        render_welcome()
        return False

    if not st.session_state["profile_complete"]:
        render_profile_setup()
        return False

    return True


def render_sidebar() -> None:
    st.sidebar.title(APP_TITLE)

    is_paid_pro = bool(st.session_state.get("premium_access", False))
    has_dev_pro = bool(st.session_state.get("dev_pro_access", False))

    plan_label = "Pro"
    plan_subtext = "Execution tools unlocked"

    if not is_paid_pro:
        plan_label = "Free"
        plan_subtext = "Core access"
        if has_dev_pro:
            plan_label = "Pro"
            plan_subtext = "Developer override enabled"

    st.sidebar.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(46,107,230,0.12), rgba(46,107,230,0.04));
            border: 1px solid rgba(46,107,230,0.22);
            border-radius: 18px;
            padding: 0.95rem 1rem 0.9rem 1rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
        ">
            <div style="
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #6b7280;
                margin-bottom: 0.38rem;
            ">
                Your Plan
            </div>
            <div style="
                display: inline-block;
                padding: 0.22rem 0.58rem;
                border-radius: 999px;
                background: rgba(46,107,230,0.10);
                border: 1px solid rgba(46,107,230,0.18);
                color: #2e6be6;
                font-size: 0.7rem;
                font-weight: 800;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                margin-bottom: 0.45rem;
            ">
                {plan_label}
            </div>
            <div style="
                font-size: 0.92rem;
                line-height: 1.45;
                color: #374151;
            ">
                {plan_subtext}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current_page = st.session_state["current_page"]
    sidebar_default = current_page if current_page in SIDEBAR_PAGES else DEFAULT_PAGE
    current_index = SIDEBAR_PAGES.index(sidebar_default) if sidebar_default in SIDEBAR_PAGES else 0

    selected_page = st.sidebar.radio(
        "Go to section:",
        options=SIDEBAR_PAGES,
        index=current_index,
    )

    if current_page in SIDEBAR_PAGES:
        st.session_state["current_page"] = selected_page
    else:
        st.sidebar.caption(f"Current page: {current_page}")

    st.sidebar.markdown("---")
    st.sidebar.caption("Developer access")

    dev_enabled = st.sidebar.checkbox(
        "Enable Pro dev access",
        value=bool(st.session_state.get("dev_pro_access", False)),
        key="sidebar_dev_pro_access",
    )
    st.session_state["dev_pro_access"] = bool(dev_enabled)

    render_reset_controls()


def render_reset_controls() -> None:
    with st.sidebar.expander("Reset assessment"):
        st.caption("This clears assessment progress and keeps your basic profile info.")

        confirm_reset = st.checkbox(
            "I understand this will reset my assessment progress.",
            key="confirm_reset_assessment",
        )

        reset_clicked = st.button(
            "Reset now",
            type="secondary",
            disabled=not confirm_reset,
            use_container_width=True,
        )

        if reset_clicked:
            reset_assessment_state(keys_to_keep=RESET_KEYS_TO_KEEP)
            st.session_state["current_page"] = DEFAULT_PAGE
            st.session_state["confirm_reset_assessment"] = False
            st.rerun()


def get_current_page() -> str:
    page = st.session_state.get("current_page", DEFAULT_PAGE)
    if page not in PAGES:
        return DEFAULT_PAGE
    return page


def render_current_page(page: str) -> None:
    renderer = PAGE_RENDERERS.get(page)

    if renderer is None:
        st.error(f'No renderer is registered for page "{page}".')
        return

    renderer()


def main() -> None:
    configure_app()
    ensure_required_state()
    render_app_header()

    if not render_gates():
        st.stop()

    render_sidebar()

    page = get_current_page()

    render_profile_strip()
    st.markdown("---")

    if not guard_page_or_warn(page):
        render_page_nav(PAGES, page)
        st.stop()

    render_current_page(page)
    render_page_nav(PAGES, page)


if __name__ == "__main__":
    main()
