# ui_styles.py

from __future__ import annotations

import html

import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                max-width: 1120px;
                padding-top: 1.25rem;
                padding-bottom: 2rem;
            }

            .rc-shell {
                width: 100%;
                margin: 0 auto;
            }

            .rc-eyebrow {
                display: inline-block;
                font-size: 0.74rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #6b7280;
                margin-bottom: 0.85rem;
            }

            .rc-title {
                font-size: clamp(2.2rem, 4.4vw, 4rem);
                font-weight: 800;
                line-height: 1.08;
                letter-spacing: -0.03em;
                color: #111827;
                max-width: 15ch;
                margin-bottom: 0.8rem;
            }

            .rc-title-wide {
                max-width: 24ch;
            }

            .rc-subtitle {
                max-width: 820px;
                font-size: 1.02rem;
                line-height: 1.7;
                color: #4b5563;
                margin-bottom: 0;
            }

            .rc-card,
            .rc-panel {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
                box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
                padding: 1.15rem 1.15rem 1.05rem 1.15rem;
            }

            .rc-card-label {
                display: inline-block;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #6b7280;
                margin-bottom: 0.45rem;
            }

            .rc-card-title {
                font-size: 1.02rem;
                font-weight: 750;
                line-height: 1.3;
                color: #111827;
                margin-bottom: 0.35rem;
            }

            .rc-card-body {
                font-size: 0.95rem;
                line-height: 1.6;
                color: #4b5563;
            }

            .rc-section-title {
                font-size: 1.3rem;
                font-weight: 750;
                line-height: 1.3;
                color: #111827;
                margin-bottom: 0.3rem;
            }

            .rc-section-body {
                font-size: 0.97rem;
                line-height: 1.65;
                color: #4b5563;
                max-width: 760px;
            }

            .rc-gap-sm { height: 0.6rem; }
            .rc-gap-md { height: 1rem; }
            .rc-gap-lg { height: 1.5rem; }

            .stButton > button {
                border-radius: 12px;
                font-weight: 700;
                min-height: 2.8rem;
            }

            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox div[data-baseweb="select"] > div,
            .stNumberInput input {
                border-radius: 12px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def open_shell() -> None:
    st.markdown('<div class="rc-shell">', unsafe_allow_html=True)


def close_shell() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def render_page_header(*, eyebrow: str, title: str, subtitle: str, wide: bool = False) -> None:
    title_class = "rc-title rc-title-wide" if wide else "rc-title"
    st.markdown(
        f"""
        <div class="rc-eyebrow">{html.escape(eyebrow)}</div>
        <div class="{title_class}">{html.escape(title)}</div>
        <div class="rc-subtitle">{html.escape(subtitle)}</div>
        """,
        unsafe_allow_html=True,
    )


def render_card(*, label: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="rc-card">
            <div class="rc-card-label">{html.escape(label)}</div>
            <div class="rc-card-title">{html.escape(title)}</div>
            <div class="rc-card-body">{html.escape(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_intro(*, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="rc-section-title">{html.escape(title)}</div>
        <div class="rc-section-body">{html.escape(body)}</div>
        """,
        unsafe_allow_html=True,
    )


# app.py change:
#
# from ui_styles import inject_global_styles
#
# def configure_app() -> None:
#     st.set_page_config(page_title=APP_TITLE, layout="wide")
#     apply_theme()
#     initialize_app_state()
#     inject_global_styles()


# Example of gradually updating one screen:
#
# from ui_styles import close_shell, open_shell, render_card, render_page_header
#
# def render_some_screen() -> None:
#     open_shell()
#     render_page_header(
#         eyebrow="Assessment",
#         title="Evaluate this opportunity with more clarity.",
#         subtitle="Use a structured review to assess fit, risk, and decision readiness.",
#         wide=True,
#     )
#     st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)
#
#     col1, col2 = st.columns(2, gap="large")
#     with col1:
#         render_card(
#             label="Fit",
#             title="Personal alignment",
#             body="Assess whether the opportunity matches your goals, capacity, and ownership style.",
#         )
#     with col2:
#         render_card(
#             label="Risk",
#             title="Financial exposure",
#             body="Review assumptions, downside exposure, and practical readiness before moving forward.",
#         )
#
#     close_shell()
