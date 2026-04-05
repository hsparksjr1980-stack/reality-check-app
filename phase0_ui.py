# phase0_ui.py

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from ui_styles import (
    close_shell,
    open_shell,
    render_card,
    render_page_header,
    render_section_intro,
)


ANSWER_OPTIONS = ["Select one...", "Yes", "Somewhat", "No"]


@dataclass(frozen=True)
class QuestionGroup:
    title: str
    description: str
    questions: tuple[str, ...]


QUESTION_GROUPS: tuple[QuestionGroup, ...] = (
    QuestionGroup(
        title="Ownership & Operating Reality",
        description="Assess whether your expectations match the day-to-day demands of ownership.",
        questions=(
            "1. Are you clear on whether you want to be an operator or mainly an investor?",
            "2. Are you willing to run daily operations if that is what the business requires early?",
            "3. Are you willing to work long hours early if needed?",
            "4. Are you comfortable managing people, turnover, and training?",
            "5. Are you willing to learn skill gaps like accounting, marketing, and staffing?",
            "6. Are you willing to be involved in sales and local marketing if traffic is slower than expected?",
        ),
    ),
    QuestionGroup(
        title="Personal Fit & Lifestyle",
        description="Evaluate whether the business aligns with your time, energy, and family reality.",
        questions=(
            "7. Are you comfortable with inventory, operational details, and repetitive execution?",
            "8. Are you naturally comfortable dealing with people all day?",
            "9. Do you have support at home for the time and stress this may require?",
            "10. Can you tolerate sustained uncertainty and stress?",
            "11. Could you handle slower-than-expected cash flow early?",
            "12. Could you handle a meaningful buildout overrun without the deal breaking?",
        ),
    ),
    QuestionGroup(
        title="Risk & Financial Exposure",
        description="Pressure test your understanding of guarantees, lease obligations, and downside exposure.",
        questions=(
            "13. Do you understand what a personal guarantee can mean for your finances?",
            "14. Do you understand lease exposure and how long it can last?",
            "15. Do you understand that personal assets may still be exposed in certain structures?",
            "16. Could you handle an income drop or delayed owner pay early on?",
            "17. Are you willing to trade convenience and flexibility for business demands for a period of time?",
            "18. Are you comfortable solving problems daily without clear answers?",
        ),
    ),
    QuestionGroup(
        title="People & Execution",
        description="Consider whether you can handle the practical realities of labor, systems, and repetition.",
        questions=(
            "19. Do you understand how hard staffing may be in a people-heavy business?",
            "20. Do you understand how disruptive turnover can be?",
            "21. Are you separating emotional excitement from business reality?",
            "22. Are you willing to walk away if the facts do not hold up?",
            "23. Are you comfortable following systems and process consistently?",
            "24. Can you handle conflict with staff, customers, vendors, or partners directly?",
        ),
    ),
    QuestionGroup(
        title="Resilience & Decision Discipline",
        description="Check whether you can stay steady if the deal is slower, harder, or more expensive than expected.",
        questions=(
            "25. Are you okay with repetitive work rather than constant novelty?",
            "26. Could you tolerate a slow ramp without panicking into bad decisions?",
            "27. Can you handle margin pressure without immediately feeling like the deal failed?",
            "28. Could you absorb unplanned expenses without the business becoming an emergency?",
            "29. Do you have a real support system, not just people cheering you on?",
            "30. Is your reason for doing this grounded in business logic, not just timing or emotion?",
        ),
    ),
)


def _answer_points(value: str) -> int:
    if value == "Yes":
        return 5
    if value == "Somewhat":
        return 3
    if value == "No":
        return 1
    return 0


def _get_result_tone(score: int) -> tuple[str, str]:
    if score >= 78:
        return "Stronger readiness signal", "Your current inputs suggest a stronger baseline fit for moving forward carefully."
    if score >= 58:
        return "Mixed readiness signal", "Some inputs support moving forward, but several areas deserve closer scrutiny."
    return "Lower readiness signal", "Your current inputs suggest more friction between this opportunity and your real operating situation."


def _metric_status_label(score: int) -> str:
    if score >= 78:
        return "Strong"
    if score >= 58:
        return "Mixed"
    return "Caution"


def _score_from_answers() -> tuple[int, str, str, list[str], list[str], int, int]:
    strengths: list[str] = []
    watchouts: list[str] = []

    ownership_style = st.session_state.get("ownership_style", "Owner-Operator")
    time_score = st.session_state.get("time_availability_score", 3)
    ops_score = st.session_state.get("operational_willingness_score", 3)
    people_score = st.session_state.get("people_management_comfort_score", 3)
    risk_score = st.session_state.get("risk_tolerance_score", 3)
    capital_score = st.session_state.get("capital_flexibility_score", 3)

    yes_no_keys = [f"rc_q{i}" for i in range(1, 31)]
    values = [st.session_state.get(key, "Select one...") for key in yes_no_keys]
    points = [_answer_points(value) for value in values]

    answered_count = sum(1 for value in values if value != "Select one...")
    total_questions = len(yes_no_keys)
    total_points = sum(points)

    quality_ratio = (total_points / (answered_count * 5)) if answered_count > 0 else 0
    completion_ratio = answered_count / total_questions

    score = 20 + round(quality_ratio * 55) + round(completion_ratio * 15)

    if ownership_style == "Owner-Operator":
        score += 5
        strengths.append("Your ownership posture appears more aligned with direct early-stage involvement.")
    elif ownership_style == "Investor / Semi-Absentee":
        watchouts.append("Semi-absentee expectations may not align well with concepts that require heavy owner involvement early.")

    if time_score >= 4:
        score += 6
        strengths.append("Your time availability appears better aligned with early owner demands.")
    elif time_score <= 2:
        watchouts.append("Limited time availability may create strain if the business requires heavier owner involvement.")

    if ops_score >= 4:
        score += 5
        strengths.append("You appear more willing to be hands-on operationally.")
    elif ops_score <= 2:
        watchouts.append("Lower operational willingness may create mismatch in higher-touch businesses.")

    if people_score >= 4:
        score += 4
        strengths.append("Higher comfort with people management may help in labor-heavy concepts.")
    elif people_score <= 2:
        watchouts.append("If people management is not a strength, team-heavy models deserve extra caution.")

    if capital_score >= 4:
        score += 6
        strengths.append("Stronger capital flexibility provides more room if reality moves against the plan.")
    elif capital_score <= 2:
        watchouts.append("Tight capital flexibility leaves less room for delays, overruns, or a slower ramp.")

    if risk_score <= 2:
        watchouts.append("A more conservative risk profile can conflict with models that depend on optimistic assumptions.")
    else:
        score += 2

    signed_anything = bool(st.session_state.get("signed_anything", False))
    if signed_anything:
        watchouts.append("Once documents are signed or money is committed, it becomes harder to unwind a weak opportunity.")
    else:
        strengths.append("You still appear early enough in the process to slow down and verify key facts.")

    if st.session_state.get("rc_q13", "Somewhat") == "No":
        watchouts.append("Weak understanding of personal guarantee exposure is a meaningful red flag.")
    if st.session_state.get("rc_q14", "Somewhat") == "No":
        watchouts.append("Limited understanding of lease exposure can create risk beyond the business itself.")
    if st.session_state.get("rc_q22", "Somewhat") == "No":
        watchouts.append("If you are not willing to walk away, emotional commitment can override discipline.")

    score = max(1, min(100, score))
    verdict, verdict_body = _get_result_tone(score)

    deduped_strengths: list[str] = []
    seen_strengths: set[str] = set()
    for item in strengths:
        if item not in seen_strengths:
            deduped_strengths.append(item)
            seen_strengths.add(item)

    deduped_watchouts: list[str] = []
    seen_watchouts: set[str] = set()
    for item in watchouts:
        if item not in seen_watchouts:
            deduped_watchouts.append(item)
            seen_watchouts.add(item)

    return (
        score,
        verdict,
        verdict_body,
        deduped_strengths[:6],
        deduped_watchouts[:6],
        answered_count,
        total_questions,
    )


def _render_live_progress(score: int, verdict: str, answered_count: int, total_questions: int) -> None:
    progress_ratio = answered_count / total_questions if total_questions else 0

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        render_card(
            label="Current score",
            title=str(score),
            body="A directional signal based on your current answers and scoring inputs.",
        )
    with col2:
        render_card(
            label="Signal",
            title=verdict,
            body="This will tighten as you complete more of the assessment.",
        )
    with col3:
        render_card(
            label="Completion",
            title=f"{answered_count} of {total_questions}",
            body="Finish all sections for a more reliable read.",
        )

    st.progress(progress_ratio)


def _render_core_inputs() -> None:
    render_section_intro(
        title="Core scoring inputs",
        body="These inputs shape the score alongside the question set. Keep them realistic, not aspirational.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.selectbox(
            "Ownership Style",
            ["Owner-Operator", "Manager-Led", "Investor / Semi-Absentee"],
            key="ownership_style",
        )
        st.slider(
            "Time Availability",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("time_availability_score", 3)),
            key="time_availability_score",
            help="1 = very limited, 5 = fully available",
        )
        st.slider(
            "Operational Willingness",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("operational_willingness_score", 3)),
            key="operational_willingness_score",
            help="1 = prefers not to run daily operations, 5 = very hands-on",
        )

    with col2:
        st.slider(
            "People Management Comfort",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("people_management_comfort_score", 3)),
            key="people_management_comfort_score",
            help="1 = not comfortable, 5 = very comfortable",
        )
        st.slider(
            "Risk Tolerance",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("risk_tolerance_score", 3)),
            key="risk_tolerance_score",
            help="1 = conservative, 5 = aggressive",
        )
        st.slider(
            "Capital Flexibility",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("capital_flexibility_score", 3)),
            key="capital_flexibility_score",
            help="1 = tight capital, 5 = strong flexibility",
        )

    st.checkbox(
        "I have already signed something or materially committed in the process",
        value=bool(st.session_state.get("signed_anything", False)),
        key="signed_anything",
    )


def _render_question_groups() -> None:
    render_section_intro(
        title="Reality Check questions",
        body="Answer based on what is true today. The goal is not optimism. The goal is fit, readiness, and discipline.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    for group_index, group in enumerate(QUESTION_GROUPS, start=1):
        with st.expander(f"{group_index}. {group.title}", expanded=(group_index == 1)):
            st.caption(group.description)
            for question in group.questions:
                question_number = int(question.split(".", 1)[0])
                st.selectbox(
                    question,
                    ANSWER_OPTIONS,
                    key=f"rc_q{question_number}",
                )


def _render_reflection_notes() -> None:
    render_section_intro(
        title="Reflection notes",
        body="These notes matter. They often reveal more than the score when someone is forcing fit.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.text_area(
        "What is the biggest reason this opportunity appeals to you right now?",
        value=st.session_state.get("rc_biggest_appeal", ""),
        key="rc_biggest_appeal",
        height=100,
        placeholder="Examples: independence, income potential, lifestyle, brand appeal, growth opportunity",
    )
    st.text_area(
        "What is your biggest concern at this stage?",
        value=st.session_state.get("rc_biggest_concern", ""),
        key="rc_biggest_concern",
        height=100,
        placeholder="Examples: risk, hours, debt, staffing, uncertainty, family impact, capital exposure",
    )
    st.text_area(
        "What would need to be true for this to fit you well?",
        value=st.session_state.get("rc_fit_conditions_notes", ""),
        key="rc_fit_conditions_notes",
        height=100,
        placeholder="Examples: manageable staffing, enough liquidity, realistic hours, family support, clear economics",
    )


def _render_results(
    *,
    score: int,
    verdict: str,
    verdict_body: str,
    strengths: list[str],
    watchouts: list[str],
) -> None:
    st.session_state["readiness_score"] = score
    st.session_state["phase_0_complete"] = True

    render_section_intro(
        title="Current result",
        body="This is a directional output, not a final decision. Treat it as a disciplined read on your present fit and readiness.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        render_card(
            label="Readiness signal",
            title=verdict,
            body=verdict_body,
        )
    with col2:
        next_signal = (
            "Continue to Concept Validation"
            if score >= 55
            else "Continue carefully and pressure test fit more aggressively"
        )
        render_card(
            label="Next step",
            title=next_signal,
            body=f"Current status: {_metric_status_label(score)}.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    strength_col, watchout_col = st.columns(2, gap="large")
    with strength_col:
        st.markdown("### What looks stronger")
        if strengths:
            for item in strengths:
                st.write(f"- {item}")
        else:
            st.write("- No clear strengths identified yet.")

    with watchout_col:
        st.markdown("### What may need more scrutiny")
        if watchouts:
            for item in watchouts:
                st.write(f"- {item}")
        else:
            st.write("- No major watch-outs identified yet.")

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    render_card(
        label="Decision discipline",
        title="Do not confuse attraction with fit.",
        body=(
            "The most important question at this stage is not whether the concept sounds appealing. "
            "It is whether the actual work, pressure, and exposure fit your reality."
        ),
    )


def render_phase_0() -> None:
    score, verdict, verdict_body, strengths, watchouts, answered_count, total_questions = _score_from_answers()

    open_shell()

    render_page_header(
        eyebrow="Phase 1 — Self & Idea",
        title="Pressure test readiness before focusing on the deal itself.",
        subtitle=(
            "This stage evaluates whether your time, operating posture, risk tolerance, "
            "support system, and capital flexibility align with what the business may actually require."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    info_col_1, info_col_2, info_col_3 = st.columns(3, gap="medium")
    with info_col_1:
        render_card(
            label="Focus",
            title="Operator vs. investor fit",
            body="Clarify whether you are genuinely suited to the work, not just attracted to the idea of ownership.",
        )
    with info_col_2:
        render_card(
            label="Focus",
            title="Risk and flexibility",
            body="Assess whether your financial position can absorb delays, overruns, and uncertainty.",
        )
    with info_col_3:
        render_card(
            label="Focus",
            title="Personal reality",
            body="Evaluate family support, time demands, staffing pressure, and tolerance for operational stress.",
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_core_inputs()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_live_progress(score, verdict, answered_count, total_questions)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_question_groups()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_reflection_notes()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    score, verdict, verdict_body, strengths, watchouts, answered_count, total_questions = _score_from_answers()
    _render_results(
        score=score,
        verdict=verdict,
        verdict_body=verdict_body,
        strengths=strengths,
        watchouts=watchouts,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if st.button("Continue to Concept Validation", key="phase0_continue", use_container_width=True, type="primary"):
        st.session_state["current_page"] = "Concept Validation"
        st.rerun()

    close_shell()
