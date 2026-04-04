import streamlit as st


ANSWER_OPTIONS = ["Select one...", "Yes", "Somewhat", "No"]


def _sidebar_color(score: int):
    if score >= 78:
        return "#3cb371", "rgba(60,179,113,.12)"   # green
    elif score >= 58:
        return "#ffc107", "rgba(255,193,7,.12)"   # yellow
    else:
        return "#dc3545", "rgba(220,53,69,.12)"   # red
    

def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .rc-hero, .rc-card, .rc-featured, .rc-helper, .rc-metric, .rc-live {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            background: rgba(255,255,255,.02);
        }
        .rc-hero {
            padding: 1.3rem 1.3rem 1rem 1.3rem;
            margin-bottom: 1rem;
        }
        .rc-card, .rc-featured, .rc-helper, .rc-metric, .rc-live {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .rc-kicker {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            opacity: 0.72;
            margin-bottom: 0.4rem;
        }
        .rc-title {
            font-size: 1.9rem;
            font-weight: 700;
            line-height: 1.15;
            margin-bottom: 0.45rem;
        }
        .rc-subtitle {
            font-size: 1rem;
            opacity: 0.92;
        }
        .rc-section-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .rc-card-title {
            font-size: 1.08rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .rc-badge {
            display: inline-block;
            font-size: 0.74rem;
            font-weight: 600;
            padding: 0.22rem 0.5rem;
            border-radius: 999px;
            border: 1px solid rgba(120,120,120,.28);
            margin-bottom: 0.55rem;
        }
        .rc-big {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .rc-muted {
            opacity: 0.84;
        }
        .rc-metric-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            opacity: 0.72;
            margin-bottom: 0.2rem;
        }
        .rc-metric-value {
            font-size: 1.45rem;
            font-weight: 700;
            line-height: 1.1;
        }
        .rc-live-title {
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .result-good {
            border: 1px solid rgba(60, 179, 113, .45) !important;
            background: rgba(60, 179, 113, .10) !important;
        }
        .result-caution {
            border: 1px solid rgba(255, 193, 7, .45) !important;
            background: rgba(255, 193, 7, .10) !important;
        }
        .result-bad {
            border: 1px solid rgba(220, 53, 69, .45) !important;
            background: rgba(220, 53, 69, .10) !important;
        }
        .metric-good {
            border: 1px solid rgba(60, 179, 113, .35) !important;
            background: rgba(60, 179, 113, .08) !important;
        }
        .metric-caution {
            border: 1px solid rgba(255, 193, 7, .35) !important;
            background: rgba(255, 193, 7, .08) !important;
        }
        .metric-bad {
            border: 1px solid rgba(220, 53, 69, .35) !important;
            background: rgba(220, 53, 69, .08) !important;
        }
        .sticky-score-wrap {
            position: sticky;
            top: 0.75rem;
            z-index: 999;
            margin-bottom: 1rem;
        }
        .sticky-score-inner {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            padding: 1rem;
            background: rgba(20,20,20,.92);
            backdrop-filter: blur(8px);
            box-shadow: 0 6px 18px rgba(0,0,0,.18);
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )


def _answer_points(value: str) -> int:
    if value == "Yes":
        return 5
    if value == "Somewhat":
        return 3
    if value == "No":
        return 1
    return 0


def _get_result_class(verdict: str) -> str:
    if verdict == "Stronger Readiness Signal":
        return "result-good"
    if verdict == "Mixed Readiness Signal":
        return "result-caution"
    return "result-bad"


def _get_metric_class(score: int) -> str:
    if score >= 78:
        return "metric-good"
    if score >= 58:
        return "metric-caution"
    return "metric-bad"


def _score_from_answers() -> tuple[int, str, list[str], list[str], int, int]:
    strengths: list[str] = []
    watchouts: list[str] = []

    ownership_style = st.session_state.get("ownership_style", "Owner-Operator")
    time_score = st.session_state.get("time_availability_score", 3)
    ops_score = st.session_state.get("operational_willingness_score", 3)
    people_score = st.session_state.get("people_management_comfort_score", 3)
    risk_score = st.session_state.get("risk_tolerance_score", 3)
    capital_score = st.session_state.get("capital_flexibility_score", 3)

    yes_no_keys = [f"rc_q{i}" for i in range(1, 31)]
    values = [st.session_state.get(k, "Select one...") for k in yes_no_keys]
    points = [_answer_points(v) for v in values]
    answered_count = sum(1 for v in values if v != "Select one...")
    total_questions = len(yes_no_keys)
    total_points = sum(points)

    quality_ratio = (total_points / (answered_count * 5)) if answered_count > 0 else 0
    completion_ratio = answered_count / total_questions

    score = 20 + round(quality_ratio * 55) + round(completion_ratio * 15)

    if ownership_style == "Owner-Operator":
        score += 5
        strengths.append("Your ownership posture appears more aligned with direct early-stage involvement.")
    elif ownership_style == "Investor / Semi-Absentee":
        watchouts.append("Semi-absentee expectations can clash with how involved many concepts require owners to be early.")

    if time_score >= 4:
        score += 6
        strengths.append("Your time availability appears stronger for early owner effort.")
    elif time_score <= 2:
        watchouts.append("Limited time availability may create strain if the business needs heavy owner involvement early.")

    if ops_score >= 4:
        score += 5
        strengths.append("You appear more willing to be hands-on operationally.")
    elif ops_score <= 2:
        watchouts.append("Lower operational willingness may create mismatch in high-touch businesses.")

    if people_score >= 4:
        score += 4
        strengths.append("Higher people-management comfort may help in labor-heavy concepts.")
    elif people_score <= 2:
        watchouts.append("If people management is not a strength, team-heavy businesses deserve extra caution.")

    if capital_score >= 4:
        score += 6
        strengths.append("Stronger capital flexibility creates more room if reality moves against the plan.")
    elif capital_score <= 2:
        watchouts.append("Tight capital flexibility leaves less room for delays, overruns, or slower ramp.")

    if risk_score <= 2:
        watchouts.append("A conservative risk profile can clash with concepts that depend on optimistic assumptions.")
    else:
        score += 2

    signed_anything = st.session_state.get("signed_anything", False)
    if signed_anything:
        watchouts.append("Once something is signed or money is committed, it becomes harder to unwind a weak deal.")
    else:
        strengths.append("You still appear early enough in the process to slow down and verify key facts.")

    if st.session_state.get("rc_q13", "Somewhat") == "No":
        watchouts.append("Weak understanding of personal guarantee exposure is a meaningful red flag.")
    if st.session_state.get("rc_q14", "Somewhat") == "No":
        watchouts.append("Limited understanding of lease exposure can create risk beyond the business itself.")
    if st.session_state.get("rc_q22", "Somewhat") == "No":
        watchouts.append("If you are not willing to walk away, emotional commitment can override discipline.")

    score = max(1, min(100, score))

    if score >= 78:
        verdict = "Stronger Readiness Signal"
    elif score >= 58:
        verdict = "Mixed Readiness Signal"
    else:
        verdict = "Weak Readiness Signal"

    deduped_strengths = []
    seen = set()
    for item in strengths:
        if item not in seen:
            deduped_strengths.append(item)
            seen.add(item)

    deduped_watchouts = []
    seen = set()
    for item in watchouts:
        if item not in seen:
            deduped_watchouts.append(item)
            seen.add(item)

    return score, verdict, deduped_strengths[:6], deduped_watchouts[:6], answered_count, total_questions


def render_phase_0():
    _inject_styles()

    st.title("Reality Check")

    st.markdown(
        """
        <div class="rc-hero">
            <div class="rc-kicker">Phase 1 — Self & Idea</div>
            <div class="rc-title">Pressure test readiness before you focus on the deal itself.</div>
            <div class="rc-subtitle">
                The point here is not whether the concept sounds attractive. It is whether your time, operating posture,
                risk tolerance, family reality, and capital position are aligned with what the business may actually require.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### What to Look At")
    st.write("- Operator vs investor mindset")
    st.write("- Time availability and lifestyle reality")
    st.write("- Risk tolerance and financial flexibility")
    st.write("- Willingness to manage people and solve operational problems")
    st.write("- Personal guarantee and lease exposure")
    st.write("- Support system and tolerance for pressure")

    st.markdown("### What’s Common in the Industry")
    st.write("Many buyers focus on the concept before pressure testing themselves. In practice, fit with the work often matters more than excitement about the brand.")

    st.markdown("### What to Ask")
    st.write("- Do I actually want to run this kind of business, or do I just like the idea of owning it?")
    st.write("- How much time, uncertainty, and pressure can I realistically carry?")
    st.write("- Am I prepared for guarantees, lease obligations, staffing, and long hours if the plan gets harder?")
    st.write("- What part of this is emotional, and what part is grounded?")

    st.markdown("### Pressure Test")
    st.write("If the business needs more time, more staffing effort, and more capital than expected, does it still fit your reality?")

    st.markdown("---")
    st.markdown("### Core Scoring Inputs")

    c1, c2 = st.columns(2)
    with c1:
        st.selectbox(
            "Ownership Style",
            ["Owner-Operator", "Manager-Led", "Investor / Semi-Absentee"],
            key="ownership_style",
        )
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

    with c2:
        st.slider(
            "People Management Comfort",
            min_value=1,
            max_value=5,
            value=st.session_state.get("people_management_comfort_score", 3),
            key="people_management_comfort_score",
            help="1 = not comfortable, 5 = very comfortable",
        )
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
        "I have already signed something or materially committed in the process",
        value=bool(st.session_state.get("signed_anything", False)),
        key="signed_anything",
    )

    live_score, live_verdict, _, _, answered_count, total_questions = _score_from_answers()
    live_metric_class = _get_metric_class(live_score)
    border_color, bg_color = _sidebar_color(live_score)

    st.sidebar.markdown(
        f"""
        <div style="
            border: 1px solid {border_color};
            border-left: 4px solid {border_color};
            background: {bg_color};
            border-radius: 14px;
            padding: 0.75rem 0.9rem;
            margin-bottom: 0.75rem;
        ">
            <div style="font-size:0.75rem; opacity:.7;">LIVE SCORE</div>
            <div style="font-size:1.4rem; font-weight:700;">{live_score}</div>
            <div style="font-size:0.8rem; margin-top:0.25rem;">
                {answered_count} / {total_questions} answered
            </div>
            <div style="font-size:0.85rem; margin-top:0.35rem; font-weight:600;">
                {live_verdict}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

    

    st.markdown(
    f"""
    <div class="sticky-score-wrap">
        <div class="sticky-score-inner {live_metric_class}">
            <div class="rc-live-title">Live Score Summary</div>
            <div class="rc-muted">
                Current Score: <strong>{live_score}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
                Answered: <strong>{answered_count} / {total_questions}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
                Current Signal: <strong>{live_verdict}</strong>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

    st.markdown("---")
    st.markdown("### 30 Reality Check Questions")

    questions = [
        "1. Are you clear on whether you want to be an operator or mainly an investor?",
        "2. Are you willing to run daily operations if that is what the business requires early?",
        "3. Are you willing to work long hours early if needed?",
        "4. Are you comfortable managing people, turnover, and training?",
        "5. Are you willing to learn skill gaps like accounting, marketing, and staffing?",
        "6. Are you willing to be involved in sales and local marketing if traffic is slower than expected?",
        "7. Are you comfortable with inventory, operational details, and repetitive execution?",
        "8. Are you naturally comfortable dealing with people all day?",
        "9. Do you have support at home for the time and stress this may require?",
        "10. Can you tolerate sustained uncertainty and stress?",
        "11. Could you handle slower-than-expected cash flow early?",
        "12. Could you handle a meaningful buildout overrun without the deal breaking?",
        "13. Do you understand what a personal guarantee can mean for your finances?",
        "14. Do you understand lease exposure and how long it can last?",
        "15. Do you understand that personal assets may still be exposed in certain structures?",
        "16. Could you handle an income drop or delayed owner pay early on?",
        "17. Are you willing to trade convenience and flexibility for business demands for a period of time?",
        "18. Are you comfortable solving problems daily without clear answers?",
        "19. Do you understand how hard staffing may be in a people-heavy business?",
        "20. Do you understand how disruptive turnover can be?",
        "21. Are you separating emotional excitement from business reality?",
        "22. Are you willing to walk away if the facts do not hold up?",
        "23. Are you comfortable following systems and process consistently?",
        "24. Can you handle conflict with staff, customers, vendors, or partners directly?",
        "25. Are you okay with repetitive work rather than constant novelty?",
        "26. Could you tolerate a slow ramp without panicking into bad decisions?",
        "27. Can you handle margin pressure without immediately feeling like the deal failed?",
        "28. Could you absorb unplanned expenses without the business becoming an emergency?",
        "29. Do you have a real support system, not just people cheering you on?",
        "30. Is your reason for doing this grounded in business logic, not just timing or emotion?",
    ]

    col1, col2 = st.columns(2)
    for i, question in enumerate(questions, start=1):
        with col1 if i <= 15 else col2:
            st.selectbox(question, ANSWER_OPTIONS, key=f"rc_q{i}")

    st.markdown("---")
    st.markdown("### Reflection Notes")

    st.text_area(
        "What is the biggest reason this opportunity appeals to you right now?",
        value=st.session_state.get("rc_biggest_appeal", ""),
        key="rc_biggest_appeal",
        height=90,
        placeholder="Examples: independence, income potential, lifestyle, brand appeal, growth opportunity",
    )

    st.text_area(
        "What is your biggest concern at this stage?",
        value=st.session_state.get("rc_biggest_concern", ""),
        key="rc_biggest_concern",
        height=90,
        placeholder="Examples: risk, hours, debt, staffing, uncertainty, family impact, capital exposure",
    )

    st.text_area(
        "What would need to be true for this to fit you well?",
        value=st.session_state.get("rc_fit_conditions_notes", ""),
        key="rc_fit_conditions_notes",
        height=90,
        placeholder="Examples: manageable staffing, enough liquidity, realistic hours, family support, clear economics",
    )

    score, verdict, strengths, watchouts, answered_count, total_questions = _score_from_answers()
    st.session_state["readiness_score"] = score

    result_class = _get_result_class(verdict)
    metric_class = _get_metric_class(score)

    st.markdown("---")
    st.markdown(
        f"""
        <div class="rc-featured {result_class}">
            <div class="rc-badge">Current Result</div>
            <div class="rc-big">{verdict}</div>
            <div class="rc-muted">
                This result summarizes how your current operating posture, personal realities, and financial flexibility appear to line up with franchise ownership reality.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(
            f"""
            <div class="rc-metric {metric_class}">
                <div class="rc-metric-label">Readiness Score</div>
                <div class="rc-metric-value">{score}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mc2:
        next_signal = "Continue to Concept Validation" if score >= 55 else "Continue, but pressure test fit carefully"
        st.markdown(
            f"""
            <div class="rc-metric">
                <div class="rc-metric-label">Next Signal</div>
                <div class="rc-metric-value" style="font-size:1.05rem;">{next_signal}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="rc-section-title">What Looks Stronger</div>', unsafe_allow_html=True)
        if strengths:
            for item in strengths:
                st.write(f"- {item}")
        else:
            st.write("- No clear strengths identified yet.")

    with c4:
        st.markdown('<div class="rc-section-title">What May Need Work</div>', unsafe_allow_html=True)
        if watchouts:
            for item in watchouts:
                st.write(f"- {item}")
        else:
            st.write("- No major watch-outs identified yet.")

    st.markdown(
        """
        <div class="rc-helper">
            <div class="rc-card-title">What to ask yourself now</div>
            <div class="rc-muted">
                Is the opportunity attractive because it fits your reality, or because it sounds appealing from a distance?
                That distinction matters more than most buyers expect.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Continue to Concept Validation", key="phase0_continue", use_container_width=True):
        st.session_state["current_page"] = "Concept Validation"
        st.rerun()
