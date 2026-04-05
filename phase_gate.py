# phase_gate.py

from __future__ import annotations

from typing import Final

import streamlit as st

from page_config import FREE_PAGES, PRO_PAGES


PRO_UNLOCK_DECISION_KEY: Final[str] = "move_forward"
PREMIUM_ACCESS_KEY: Final[str] = "premium_access"
DEV_OVERRIDE_KEY: Final[str] = "dev_pro_access"

PRO_UNLOCK_DECISION_MESSAGE: Final[str] = (
    "Pro pages unlock only after you choose Move Forward in Final Decision."
)
PRO_PREMIUM_REQUIRED_MESSAGE: Final[str] = "This page requires Pro access."
UNKNOWN_PAGE_MESSAGE: Final[str] = "This section is not available."


def _has_dev_override() -> bool:
    return bool(st.session_state.get(DEV_OVERRIDE_KEY, False))


def _has_premium_access() -> bool:
    return bool(st.session_state.get(PREMIUM_ACCESS_KEY, False)) or _has_dev_override()


def _has_pro_unlock_decision() -> bool:
    return bool(st.session_state.get(PRO_UNLOCK_DECISION_KEY, False)) or _has_dev_override()


def is_free_page(page_name: str) -> bool:
    return page_name in FREE_PAGES


def is_pro_page(page_name: str) -> bool:
    return page_name in PRO_PAGES


def get_unlock_failure_reason(page_name: str) -> str | None:
    if is_free_page(page_name):
        return None

    if is_pro_page(page_name):
        if not _has_pro_unlock_decision():
            return PRO_UNLOCK_DECISION_MESSAGE

        if not _has_premium_access():
            return PRO_PREMIUM_REQUIRED_MESSAGE

        return None

    return UNKNOWN_PAGE_MESSAGE


def is_page_unlocked(page_name: str) -> tuple[bool, str | None]:
    reason = get_unlock_failure_reason(page_name)
    return reason is None, reason


def guard_page_or_warn(page_name: str) -> bool:
    unlocked, reason = is_page_unlocked(page_name)
    if unlocked:
        return True

    if reason:
        st.warning(reason)
    else:
        st.warning(UNKNOWN_PAGE_MESSAGE)

    return False
