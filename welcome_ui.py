# welcome_ui.py

from __future__ import annotations

import streamlit as st

from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_page_header,
)


def _select_auth_mode(mode: str) -> None:
    st.session_state["account_mode"] = mode
    st.session_state["auth_complete"] = True
    st.rerun()


def _render_auth_actions() -> None:
    col1, col2 = st.columns(2, gap="large")

    with col1:
        if st.button(
            "Create Account",
            key="create_account_button",
            use_container_width=True,
            type="primary",
        ):
            _select_auth_mode("create")

    with col2:
        if st.button(
            "Sign In",
            key="sign_in_button",
            use_container_width=True,
        ):
            _select_auth_mode("login")


def render_welcome() -> None:
    open_shell()

    render_page_header(
        eyebrow="Franchise Evaluation Platform",
        title="Make better franchise decisions before you commit.",
        subtitle=(
            "Reality Check helps you evaluate opportunity fit, financial exposure, "
            "and decision readiness with a structured, practical workflow."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        render_card(
            label="Clarity",
            title="Structured evaluation",
            body=(
                "Move from initial review to decision with a clear, consistent process."
            ),
        )

    with col2:
        render_card(
            label="Rigor",
            title="Financial perspective",
            body=(
                "Review exposure, assumptions, and readiness with greater discipline."
            ),
        )

    with col3:
        render_card(
            label="Action",
            title="Useful outputs",
            body=(
                "Get practical next-step guidance to support better decisions."
            ),
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    auth_col_1, auth_col_2 = st.columns(2, gap="large")

    with auth_col_1:
        render_card(
            label="New user",
            title="Create your account",
            body=(
                "Start a new assessment, set up your profile, and save your progress."
            ),
        )

    with auth_col_2:
        render_card(
            label="Returning user",
            title="Sign in to continue",
            body=(
                "Resume your progress, review prior inputs, and continue your assessment."
            ),
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    _render_auth_actions()

    st.caption(
        "Designed to support disciplined opportunity review without unnecessary complexity."
    )

    close_shell()
