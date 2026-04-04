import streamlit as st
from page_config import FREE_PAGES, PRO_PAGES


FREE_SEQUENCE = [
    "Overview",
    "Reality Check",
    "Concept Validation",
    "Financial Model",
    "Post-Discovery",
    "Final Decision",
]


def get_completed_pages() -> dict:
    return st.session_state.get("phase_completion", {})


def is_page_unlocked(page_name: str) -> tuple[bool, str | None]:
    if page_name in FREE_PAGES:
        return True, None

    if page_name in PRO_PAGES:
        if not (
            st.session_state.get("move_forward", False)
            or st.session_state.get("dev_pro_access", False)
        ):
            return False, "Pro pages unlock only after you choose Move Forward at Final Decision."

        if not (
            st.session_state.get("premium_access", False)
            or st.session_state.get("dev_pro_access", False)
        ):
            return False, "This page requires Pro access."

        return True, None

    return True, None


def guard_page_or_warn(page_name: str) -> bool:
    unlocked, reason = is_page_unlocked(page_name)
    if unlocked:
        return True
    st.warning(reason)
    return False
