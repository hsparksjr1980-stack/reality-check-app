import streamlit as st
from page_config import DEFAULT_PAGE


DEFAULTS = {
    "auth_complete": False,
    "profile_complete": False,
    "current_page": DEFAULT_PAGE,
    "sidebar_page_selector": DEFAULT_PAGE,
    "account_mode": None,
    "premium_access": False,
    "dev_pro_access": True,
    "decision_locked": False,
    "final_decision_action": None,
    "move_forward": False,
    "walk_away": False,
    "phase_completion": {
        "Overview": False,
        "Reality Check": False,
        "Concept Validation": False,
        "Financial Model": False,
        "Post-Discovery": False,
        "Final Decision": False,
    },
    "required_guardrails": {},
    "guardrail_status": {},
    "buildout_tracker_df": None,
    "workspace_notes": None,
}


def initialize_app_state() -> None:
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def mark_page_complete(page_name: str) -> None:
    phase_completion = st.session_state.get("phase_completion", {})
    phase_completion[page_name] = True
    st.session_state["phase_completion"] = phase_completion


def reset_assessment_state(keys_to_keep: list[str]) -> None:
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]
    initialize_app_state()
