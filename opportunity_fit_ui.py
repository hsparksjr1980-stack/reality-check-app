import streamlit as st
from opportunity_fit_engine import build_opportunity_fit_packet, PROFILE_DEFINITIONS


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .of-card {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            padding: 1rem;
            background: rgba(255,255,255,.02);
            margin-bottom: 1rem;
        }
        .of-good {
            border: 1px solid rgba(60, 179, 113, .45) !important;
            background: rgba(60, 179, 113, .10) !important;
        }
        .of-caution {
            border: 1px solid rgba(255, 193, 7, .45) !important;
            background: rgba(255, 193, 7, .10) !important;
        }
        .of-bad {
            border: 1px solid rgba(220, 53, 69, .45) !important;
            background: rgba(220, 53, 69, .10) !important;
        }
        .of-title {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .of-muted {
            opacity: 0.84;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _score_class(value: int) -> str:
    if value >= 4:
        return "of-good"
    if value == 3:
        return "of-caution"
    return "of-bad"


def _render_score_card(scores: dict) -> None:
    st.markdown("### Score Breakdown")
    labels = [
        ("Time Availability", scores["time_availability"]),
        ("Operational Willingness", scores["operational_willingness"]),
        ("People Management Comfort", scores["people_management_comfort"]),
        ("Risk Tolerance", scores["risk_tolerance"]),
        ("Capital Flexibility", scores["capital_flexibility"]),
    ]

    cols = st.columns(5)
    for col, (label, value) in zip(cols, labels):
        with col:
            css = _score_class(value)
            st.markdown(
                f"""
                <div class="of-card {css}">
                    <div class="of-title">{label}</div>
                    <div style="font-size:1.5rem;font-weight:700;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_profile_card(packet: dict) -> None:
    primary = packet["primary_profile"]
    secondary = packet["secondary_profile"]

    st.markdown("### Your Profile")
    st.markdown(
        f"""
        <div class="of-card of-good">
            <div class="of-title">Primary Profile: {primary}</div>
            <div class="of-muted">{PROFILE_DEFINITIONS[primary]["description"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if secondary:
        st.markdown(
            f"""
            <div class="of-card of-caution">
                <div class="of-title">Secondary Profile: {secondary}</div>
                <div class="of-muted">{PROFILE_DEFINITIONS[secondary]["description"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_fit_sections(packet: dict) -> None:
    st.markdown("### Business Types That May Fit You")
    for item in packet["recommended_categories"]:
        st.markdown(
            f"""
            <div class="of-card of-good">
                <div class="of-title">{item}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### What to Be Careful With")
    if packet["watchouts"]:
        for item in packet["watchouts"]:
            st.markdown(
                f"""
                <div class="of-card of-caution">
                    <div class="of-muted">{item}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="of-card of-good">
                <div class="of-muted">No major watch-outs identified yet.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Alternative Paths to Explore")
    for item in packet["alternative_paths"]:
        st.markdown(
            f"""
            <div class="of-card">
                <div class="of-muted">You may want to explore {item.lower()}.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Why These Recommendations Fit")
    for item in packet["why_fit"]:
        st.markdown(
            f"""
            <div class="of-card">
                <div class="of-muted">{item}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_opportunity_fit():
    _inject_styles()

    st.title("Opportunity Fit & Recommendations")
    st.caption("Use your inputs to understand what kinds of business models may fit you better before testing a specific concept financially.")

    st.markdown("## What to Look At")
    st.write("The goal here is not to predict success. It is to pressure test fit across time, operating style, people management, risk, and capital flexibility.")

    st.markdown("## What’s Common in the Industry")
    st.write("Many buyers focus on the concept first and their operating fit second. In practice, operator fit often matters more than the pitch deck.")

    st.markdown("## What to Ask")
    st.write("- How much time can I realistically give this business early?")
    st.write("- Do I want to run daily operations, or mainly oversee them?")
    st.write("- Am I comfortable managing people, turnover, and training?")
    st.write("- How much cost overrun or delay can I really absorb?")
    st.write("- Am I looking for an operator lifestyle or an investment structure?")

    st.markdown("## Pressure Test")
    st.write("If the concept requires more owner involvement, more staffing pressure, or more capital than expected, does it still fit how you actually want to operate?")

    st.markdown("---")
    st.markdown("## Input Calibration")
    st.write("Use these scores to reflect the answers you gave earlier. This stays at the category level and is meant to be explainable, not overly definitive.")

    c1, c2 = st.columns(2)
    with c1:
        st.slider(
            "Time Availability",
            min_value=1,
            max_value=5,
            value=st.session_state.get("time_availability_score", 3),
            key="time_availability_score",
            help="1 = very limited, 5 = fully available",
        )
        st.slider(
            "Operational Willingness",
            min_value=1,
            max_value=5,
            value=st.session_state.get("operational_willingness_score", 3),
            key="operational_willingness_score",
            help="1 = does not want daily operations, 5 = wants to be very hands-on",
        )
        st.slider(
            "People Management Comfort",
            min_value=1,
            max_value=5,
            value=st.session_state.get("people_management_comfort_score", 3),
            key="people_management_comfort_score",
            help="1 = not comfortable managing people, 5 = very comfortable",
        )

    with c2:
        st.slider(
            "Risk Tolerance",
            min_value=1,
            max_value=5,
            value=st.session_state.get("risk_tolerance_score", 3),
            key="risk_tolerance_score",
            help="1 = conservative, 5 = aggressive",
        )
        st.slider(
            "Capital Flexibility",
            min_value=1,
            max_value=5,
            value=st.session_state.get("capital_flexibility_score", 3),
            key="capital_flexibility_score",
            help="1 = tight capital, 5 = strong flexibility",
        )
        st.checkbox(
            "I generally prefer structured systems and repeatable processes",
            value=st.session_state.get("prefers_structure_process", False),
            key="prefers_structure_process",
        )

    packet = build_opportunity_fit_packet()

    st.markdown("---")
    _render_profile_card(packet)
    _render_score_card(packet["scores"])
    _render_fit_sections(packet)

    st.markdown("### Next Step")
    st.info("Now test whether a concept that fits you also works financially.")

    if st.button("Continue to Financial Model"):
        st.session_state["current_page"] = "Financial Model"
        st.rerun()
