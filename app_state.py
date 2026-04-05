# app_state.py

from __future__ import annotations

from copy import deepcopy
from typing import Any, Final

import streamlit as st

from page_config import DEFAULT_PAGE


CORE_DEFAULTS: Final[dict[str, Any]] = {
    "auth_complete": False,
    "profile_complete": False,
    "premium_access": False,
    "dev_pro_access": True,
    "current_page": DEFAULT_PAGE,
    "nav_target_page": DEFAULT_PAGE,
}

PROFILE_DEFAULTS: Final[dict[str, Any]] = {
    "full_name": "",
    "email": "",
    "city_state": "",
    "franchise_name": "",
    "units_considered": "",
    "ownership_style": "",
    "signed_anything": False,
}

ASSESSMENT_DEFAULTS: Final[dict[str, Any]] = {
    "assessment_started": False,
    "assessment_completed": False,
    "phase_0_complete": False,
    "phase_1_complete": False,
    "phase_2_complete": False,
    "phase_3_complete": False,
    "report_generated": False,
    "free_report_generated": False,
    "final_decision_submitted": False,
    "confirm_reset_assessment": False,
    "move_forward": False,
    "walk_away": False,
}

UI_DEFAULTS: Final[dict[str, Any]] = {
    "toast_message": "",
    "toast_type": "info",
}

SESSION_DEFAULTS: Final[dict[str, Any]] = {
    **CORE_DEFAULTS,
    **PROFILE_DEFAULTS,
    **ASSESSMENT_DEFAULTS,
    **UI_DEFAULTS,
}


def _clone_default(value: Any) -> Any:
    if isinstance(value, (dict, list, set)):
        return deepcopy(value)
    return value


def initialize_app_state() -> None:
    for key, default_value in SESSION_DEFAULTS.items():
        st.session_state.setdefault(key, _clone_default(default_value))
    normalize_session_state()


def normalize_session_state() -> None:
    current_page = st.session_state.get("current_page", DEFAULT_PAGE)
    if not isinstance(current_page, str) or not current_page.strip():
        st.session_state["current_page"] = DEFAULT_PAGE

    nav_target_page = st.session_state.get("nav_target_page", st.session_state["current_page"])
    if not isinstance(nav_target_page, str) or not nav_target_page.strip():
        st.session_state["nav_target_page"] = st.session_state["current_page"]

    for key in (
        "auth_complete",
        "profile_complete",
        "premium_access",
        "dev_pro_access",
        "assessment_started",
        "assessment_completed",
        "phase_0_complete",
        "phase_1_complete",
        "phase_2_complete",
        "phase_3_complete",
        "report_generated",
        "free_report_generated",
        "final_decision_submitted",
        "confirm_reset_assessment",
        "move_forward",
        "walk_away",
        "signed_anything",
    ):
        st.session_state[key] = bool(st.session_state.get(key, False))


def get_state(key: str, default: Any = None) -> Any:
    return st.session_state.get(key, default)


def set_state(**kwargs: Any) -> None:
    for key, value in kwargs.items():
        st.session_state[key] = value


def get_current_page() -> str:
    page = st.session_state.get("current_page", DEFAULT_PAGE)
    if not isinstance(page, str) or not page.strip():
        return DEFAULT_PAGE
    return page


def set_current_page(page_name: str) -> None:
    if not isinstance(page_name, str) or not page_name.strip():
        raise ValueError("page_name must be a non-empty string.")
    st.session_state["current_page"] = page_name
    st.session_state["nav_target_page"] = page_name


def has_premium_access() -> bool:
    return bool(st.session_state.get("premium_access", False))


def mark_assessment_started() -> None:
    st.session_state["assessment_started"] = True


def mark_phase_complete(phase_number: int) -> None:
    phase_key = f"phase_{phase_number}_complete"
    if phase_key not in SESSION_DEFAULTS:
        raise ValueError(f"Unsupported phase number: {phase_number}")
    st.session_state[phase_key] = True


def reset_assessment_state(keys_to_keep: list[str] | None = None) -> None:
    keep_keys = set(keys_to_keep or [])
    preserved_values = {
        key: deepcopy(st.session_state[key])
        for key in keep_keys
        if key in st.session_state
    }

    for key in list(st.session_state.keys()):
        if key not in keep_keys:
            del st.session_state[key]

    for key, default_value in SESSION_DEFAULTS.items():
        if key not in keep_keys:
            st.session_state[key] = _clone_default(default_value)

    for key, value in preserved_values.items():
        st.session_state[key] = value

    st.session_state["current_page"] = DEFAULT_PAGE
    st.session_state["nav_target_page"] = DEFAULT_PAGE
    st.session_state["confirm_reset_assessment"] = False


def clear_toasts() -> None:
    st.session_state["toast_message"] = ""
    st.session_state["toast_type"] = "info"
