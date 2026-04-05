# overview_ui.py

from __future__ import annotations

import streamlit as st

from page_config import PAGES
from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_page_header,
    render_section_intro,
)


def _go_to(page_name: str) -> None:
    st.session_state["current_page"] = page_name
    st.rerun()


def _status_label(value: bool) -> str:
    return "Complete" if value else "In Progress"


def _progress_counts() -> tuple[int, int]:
    tracked_keys = [
        "phase_0_complete",
        "phase_1_complete",
        "phase_2_complete",
        "phase_3_complete",
    ]
    completed = sum(bool(st.session_state.get(key, False)) for key in tracked_keys)
    return completed, len(tracked_keys)


def render_overview() -> None:
    completed_count, total_count = _progress_counts()
    premium_access = bool(st.session_state.get("premium_access", False))
    franchise_name = st.session_state.get("franchise_name", "").strip() or "your opportunity"

    open_shell()

    render_page_header(
        eyebrow="Overview",
        title="Review your assessment workflow at a glance.",
        subtitle=(
            f"Use this overview to track progress, revisit key sections, and continue "
            f"evaluating {franchise_name} with a structured process."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    stat_col_1, stat_col_2, stat_col_3 = st.columns(3, gap="medium")

    with stat_col_1:
        render_card(
            label="Progress",
            title=f"{completed_count} of {total_count} phases completed",
            body="Track how far you have moved through the core evaluation process.",
        )

    with stat_col_2:
        render_card(
            label="Account",
            title="Profile active",
            body="Your profile is set up and ready to support the assessment flow.",
        )

    with stat_col_3:
        render_card(
            label="Access",
            title="Pro enabled" if premium_access else "Free plan",
            body=(
                "Execution tools are available."
                if premium_access
                else "Upgrade when you are ready for deeper execution support."
            ),
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Core workflow",
        body="Move through the assessment in order, or jump back into the section you want to review.",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    workflow_col_1, workflow_col_2 = st.columns(2, gap="large")

    with workflow_col_1:
        render_card(
            label="Phase 1",
            title="Reality Check",
            body=(
                "Assess the opportunity at a high level and clarify whether it is worth "
                "continued attention."
            ),
        )
        if st.button(
            "Open Reality Check",
            key="overview_open_reality_check",
            use_container_width=True,
        ):
            _go_to("Reality Check")

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        render_card(
            label="Phase 2",
            title="Concept Validation",
            body=(
                "Pressure-test the concept and evaluate whether the business case holds "
                "up under closer review."
            ),
        )
        if st.button(
            "Open Concept Validation",
            key="overview_open_concept_validation",
            use_container_width=True,
        ):
            _go_to("Concept Validation")

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        render_card(
            label="Phase 3",
            title="Opportunity Fit & Recommendations",
            body=(
                "Review fit, practical implications, and recommendations based on your "
                "inputs and decision context."
            ),
        )
        if st.button(
            "Open Opportunity Fit & Recommendations",
            key="overview_open_opportunity_fit",
            use_container_width=True,
        ):
            _go_to("Opportunity Fit & Recommendations")

    with workflow_col_2:
        render_card(
            label="Financial",
            title="Financial Model",
            body=(
                "Review assumptions, exposure, and whether the economics appear realistic "
                "for your situation."
            ),
        )
        if st.button(
            "Open Financial Model",
            key="overview_open_financial_model",
            use_container_width=True,
        ):
            _go_to("Financial Model")

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        render_card(
            label="Decision",
            title="Final Decision",
            body=(
                "Bring the assessment together and decide whether to move forward, pause, "
                "or walk away."
            ),
        )
        if st.button(
            "Open Final Decision",
            key="overview_open_final_decision",
            use_container_width=True,
        ):
            _go_to("Final Decision")

        st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

        render_card(
            label="Output",
            title="Reports",
            body=(
                "Generate a report view that summarizes your assessment and supports "
                "follow-up discussion."
            ),
        )
        report_target = "Report" if "Report" in PAGES else "Free Report"
        if st.button(
            "Open Reports",
            key="overview_open_reports",
            use_container_width=True,
        ):
            _go_to(report_target)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    render_section_intro(
        title="Current status",
        body="A simple snapshot of where you are in the process right now.",
    )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    status_col_1, status_col_2, status_col_3, status_col_4 = st.columns(4, gap="medium")

    with status_col_1:
        render_card(
            label="Reality Check",
            title=_status_label(bool(st.session_state.get("phase_0_complete", False))),
            body="Initial opportunity screen.",
        )

    with status_col_2:
        render_card(
            label="Concept Validation",
            title=_status_label(bool(st.session_state.get("phase_1_complete", False))),
            body="Deeper concept review.",
        )

    with status_col_3:
        render_card(
            label="Post-Discovery",
            title=_status_label(bool(st.session_state.get("phase_2_complete", False))),
            body="Pre-commitment diligence.",
        )

    with status_col_4:
        render_card(
            label="Final Decision",
            title=_status_label(bool(st.session_state.get("phase_3_complete", False))),
            body="Decision readiness summary.",
        )

    close_shell()
