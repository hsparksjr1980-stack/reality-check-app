# profile_ui.py

from __future__ import annotations

import streamlit as st

from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_page_header,
    render_section_intro,
)


UNITS_OPTIONS = ["1", "2-3", "4+"]
OWNERSHIP_OPTIONS = [
    "Owner-Operator",
    "Manager-Led",
    "Investor / Semi-Absentee",
]


def _get_index(options: list[str], value: str, default: str) -> int:
    selected = value if value in options else default
    return options.index(selected)


def _complete_profile() -> None:
    st.session_state["profile_complete"] = True
    st.session_state["current_page"] = "Overview"
    st.rerun()


def render_profile_setup() -> None:
    open_shell()

    render_page_header(
        eyebrow="Getting Started",
        title="Set up your profile before starting the evaluation.",
        subtitle=(
            "Provide a few basics so the assessment can guide your decision flow "
            "with better context."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Basic Information",
        body="Keep this simple for now. You can refine details later.",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    info_col_1, info_col_2 = st.columns(2, gap="large")

    with info_col_1:
        st.text_input(
            "Full Name",
            value=st.session_state.get("full_name", ""),
            key="full_name",
            placeholder="Enter your full name",
        )
        st.text_input(
            "Email",
            value=st.session_state.get("email", ""),
            key="email",
            placeholder="Enter your email",
        )
        st.text_input(
            "City / State",
            value=st.session_state.get("city_state", ""),
            key="city_state",
            placeholder="City, State",
        )

    with info_col_2:
        st.text_input(
            "Franchise or Concept Name",
            value=st.session_state.get("franchise_name", ""),
            key="franchise_name",
            placeholder="Enter franchise or concept name",
        )
        st.selectbox(
            "Units Considered",
            UNITS_OPTIONS,
            index=_get_index(
                UNITS_OPTIONS,
                st.session_state.get("units_considered", "1"),
                "1",
            ),
            key="units_considered",
        )
        st.selectbox(
            "Ownership Style",
            OWNERSHIP_OPTIONS,
            index=_get_index(
                OWNERSHIP_OPTIONS,
                st.session_state.get("ownership_style", "Owner-Operator"),
                "Owner-Operator",
            ),
            key="ownership_style",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    render_card(
        label="Commitment Check",
        title="Current process status",
        body=(
            "Indicate whether you have already signed documents or made a material "
            "commitment in the process."
        ),
    )

    st.markdown('<div class="rc-gap-sm"></div>', unsafe_allow_html=True)

    st.checkbox(
        "I have already signed something or materially committed in the process",
        value=bool(st.session_state.get("signed_anything", False)),
        key="signed_anything",
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    action_col_1, action_col_2 = st.columns([1, 1], gap="large")

    with action_col_1:
        if st.button(
            "Continue",
            key="profile_setup_continue",
            use_container_width=True,
            type="primary",
        ):
            _complete_profile()

    with action_col_2:
        st.caption("You can update these details later.")

    close_shell()
