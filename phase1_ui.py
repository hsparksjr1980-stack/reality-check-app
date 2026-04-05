# phase1_ui.py

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
        title="Market Demand",
        description="Assess whether there is credible local demand beyond surface enthusiasm.",
        questions=(
            "1. Is there a clear and recurring customer need for this concept in your target market?",
            "2. Does the concept solve a real problem or serve a durable demand pattern?",
            "3. Is the target customer easy to identify and describe clearly?",
            "4. Does the concept appear resilient beyond a short-term trend or novelty cycle?",
            "5. Is there enough local population density, traffic, or reach to support demand?",
            "6. Does the concept appear relevant for the demographics in your target market?",
        ),
    ),
    QuestionGroup(
        title="Competition & Positioning",
        description="Evaluate whether the concept can hold a credible place in the local market.",
        questions=(
            "7. Is the competitive landscape understandable rather than crowded and unclear?",
            "8. Does the concept have a meaningful point of differentiation from alternatives?",
            "9. Would a customer have a clear reason to choose this option over others?",
            "10. Is pricing likely to be competitive without destroying margins?",
            "11. Are you comfortable with how directly this concept competes in the market?",
            "12. Does the brand positioning feel credible rather than marketing-driven only?",
        ),
    ),
    QuestionGroup(
        title="Unit Economics & Practical Model",
        description="Pressure test whether the business model appears realistic in practice.",
        questions=(
            "13. Do the revenue assumptions appear plausible rather than optimistic?",
            "14. Do labor requirements appear manageable for the business model?",
            "15. Do occupancy, lease, or location economics seem realistic for your market?",
            "16. Does the model appear capable of producing acceptable margins after real expenses?",
            "17. Is the operating complexity manageable for the expected return?",
            "18. Does the path to breakeven seem credible within a reasonable timeframe?",
        ),
    ),
    QuestionGroup(
        title="Franchisor & System Quality",
        description="Review whether the system appears capable of supporting execution responsibly.",
        questions=(
            "19. Does the franchisor appear organized and credible in how it presents the opportunity?",
            "20. Does the support model appear practical rather than mostly promotional?",
            "21. Do training and onboarding appear sufficient for real operating demands?",
            "22. Does the brand appear honest about risks, not only upside?",
            "23. Are system standards and expectations clear enough to execute consistently?",
            "24. Does the franchisor appear selective enough to protect system quality?",
        ),
    ),
    QuestionGroup(
        title="Decision Discipline",
        description="Check whether the decision is being grounded in evidence instead of momentum.",
        questions=(
            "25. Are you evaluating this concept based on facts rather than enthusiasm alone?",
            "26. Are you willing to reject the opportunity if the economics do not hold up?",
            "27. Are you separating brand appeal from actual business quality?",
            "28. Do you believe your assumptions have been tested rather than merely hoped for?",
            "29. Would this still be attractive if ramp-up is slower and costs are higher than expected?",
            "30. Does the opportunity still make sense after considering downside scenarios?",
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


def _status_label(score: int) -> str:
    if score >= 78:
        return "Strong"
    if score >= 58:
        return "Mixed"
    return "Caution"


def _result_summary(score: int) -> tuple[str, str]:
    if score >= 78:
        return (
            "Stronger validation signal",
            "The current inputs support a more credible case for continuing, while still requiring disciplined verification.",
        )
    if score >= 58:
        return (
            "Mixed validation signal",
            "Some elements appear workable, but several assumptions still need tighter scrutiny before confidence is justified.",
        )
    return (
        "Weaker validation signal",
        "The current inputs suggest the concept may be less robust than it first appears and deserves closer pressure testing.",
    )


def _score_from_answers() -> tuple[int, str, str, list[str], list[str], int, int]:
    strengths: list[str] = []
    watchouts: list[str] = []

    market_score = int(st.session_state.get("cv_market_confidence_score", 3))
    competition_score = int(st.session_state.get("cv_competition_position_score", 3))
    economics_score = int(st.session_state.get("cv_economic_confidence_score", 3))
    support_score = int(st.session_state.get("cv_support_confidence_score", 3))
    discipline_score = int(st.session_state.get("cv_decision_discipline_score", 3))

    answer_keys = [f"cv_q{i}" for i in range(1, 31)]
    values = [st.session_state.get(key, "Select one...") for key in answer_keys]
    points = [_answer_points(value) for value in values]

    answered_count = sum(1 for value in values if value != "Select one...")
    total_questions = len(answer_keys)
    total_points = sum(points)

    quality_ratio = (total_points / (answered_count * 5)) if answered_count > 0 else 0
    completion_ratio = answered_count / total_questions

    score = 20 + round(quality_ratio * 55) + round(completion_ratio * 15)

    if market_score >= 4:
        score += 6
        strengths.append("You appear to have stronger confidence in underlying market demand.")
    elif market_score <= 2:
        watchouts.append("If local demand is uncertain, the concept may be harder to support than it appears on paper.")

    if competition_score >= 4:
        score += 5
        strengths.append("The concept appears better positioned against local competition.")
    elif competition_score <= 2:
        watchouts.append("Weak differentiation can make growth and pricing discipline harder to sustain.")

    if economics_score >= 4:
        score += 7
        strengths.append("Your current read on the unit economics appears more credible.")
    elif economics_score <= 2:
        watchouts.append("If the economics feel thin now, they may look worse under real operating pressure.")

    if support_score >= 4:
        score += 4
        strengths.append("The system appears more likely to support execution in a practical way.")
    elif support_score <= 2:
        watchouts.append("If support is unclear or weak, operating risk may shift more heavily to you.")

    if discipline_score >= 4:
        score += 4
        strengths.append("Your decision posture appears more evidence-based and disciplined.")
    elif discipline_score <= 2:
        watchouts.append("Momentum and optimism may be carrying too much of the decision process.")

    if st.session_state.get("cv_q13", "Somewhat") == "No":
        watchouts.append("Unconvincing revenue assumptions are a serious warning sign.")
    if st.session_state.get("cv_q16", "Somewhat") == "No":
        watchouts.append("If margins do not appear acceptable after real expenses, the opportunity may not justify the effort.")
    if st.session_state.get("cv_q22", "Somewhat") == "No":
        watchouts.append("If risks are not being presented honestly, that reduces confidence in the system.")
    if st.session_state.get("cv_q26", "Somewhat") == "No":
        watchouts.append("If you are not willing to reject the deal, discipline can erode quickly.")
    if st.session_state.get("cv_q30", "Somewhat") == "Yes":
        strengths.append("The opportunity may still hold up better after downside scenarios are considered.")

    score = max(1, min(100, score))
    verdict, verdict_body = _result_summary(score)

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
            body="A directional signal based on your present answers and scoring inputs.",
        )
    with col2:
        render_card(
            label="Signal",
            title=verdict,
            body="This becomes more reliable as the full section is completed.",
        )
    with col3:
        render_card(
            label="Completion",
            title=f"{answered_count} of {total_questions}",
            body="Complete every section for a stronger validation read.",
        )

    st.progress(progress_ratio)


def _render_core_inputs() -> None:
    render_section_intro(
        title="Core validation inputs",
        body="Use these higher-level inputs to reflect your current level of confidence. Keep them grounded in evidence.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.slider(
            "Market Confidence",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("cv_market_confidence_score", 3)),
            key="cv_market_confidence_score",
            help="1 = weak confidence, 5 = strong confidence",
        )
        st.slider(
            "Competition / Positioning Confidence",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("cv_competition_position_score", 3)),
            key="cv_competition_position_score",
            help="1 = weak position, 5 = strong position",
        )
        st.slider(
            "Economic Confidence",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("cv_economic_confidence_score", 3)),
            key="cv_economic_confidence_score",
            help="1 = weak economics, 5 = strong economics",
        )

    with col2:
        st.slider(
            "Support Confidence",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("cv_support_confidence_score", 3)),
            key="cv_support_confidence_score",
            help="1 = weak support, 5 = strong support",
        )
        st.slider(
            "Decision Discipline",
            min_value=1,
            max_value=5,
            value=int(st.session_state.get("cv_decision_discipline_score", 3)),
            key="cv_decision_discipline_score",
            help="1 = emotional / rushed, 5 = disciplined / evidence-based",
        )

        st.text_input(
            "Target Market",
            value=st.session_state.get("cv_target_market", ""),
            key="cv_target_market",
            placeholder="City, trade area, or market description",
        )


def _render_question_groups() -> None:
    render_section_intro(
        title="Concept validation questions",
        body="Answer based on what you can defend with evidence today. This stage is about pressure testing assumptions, not confirming excitement.",
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
                    key=f"cv_q{question_number}",
                )


def _render_notes() -> None:
    render_section_intro(
        title="Supporting notes",
        body="Capture the points that are making the concept stronger or weaker in your mind.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.text_area(
        "What evidence currently supports local demand?",
        value=st.session_state.get("cv_demand_notes", ""),
        key="cv_demand_notes",
        height=100,
        placeholder="Examples: observed traffic, market gaps, demographics, comparable businesses, repeat demand",
    )
    st.text_area(
        "What are the biggest weaknesses or open questions in the concept right now?",
        value=st.session_state.get("cv_risk_notes", ""),
        key="cv_risk_notes",
        height=100,
        placeholder="Examples: competition, margins, staffing, pricing pressure, location risk, franchisor support",
    )
    st.text_area(
        "What would you need to verify before confidence would materially improve?",
        value=st.session_state.get("cv_verification_notes", ""),
        key="cv_verification_notes",
        height=100,
        placeholder="Examples: economics, market demand, labor model, lease assumptions, operational complexity",
    )


def _render_results(
    *,
    score: int,
    verdict: str,
    verdict_body: str,
    strengths: list[str],
    watchouts: list[str],
) -> None:
    st.session_state["concept_validation_score"] = score
    st.session_state["phase_1_complete"] = True

    render_section_intro(
        title="Current result",
        body="Use this output as a structured read on concept quality and decision discipline, not as proof that the deal works.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        render_card(
            label="Validation signal",
            title=verdict,
            body=verdict_body,
        )

    with col2:
        next_step = (
            "Continue to Opportunity Fit & Recommendations"
            if score >= 55
            else "Continue carefully and validate the weaker assumptions first"
        )
        render_card(
            label="Next step",
            title=next_step,
            body=f"Current status: {_status_label(score)}.",
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
        title="Do not let brand appeal replace evidence.",
        body=(
            "A concept can look polished, familiar, or exciting and still be weak in your market or under real operating conditions."
        ),
    )


def render_phase_1() -> None:
    score, verdict, verdict_body, strengths, watchouts, answered_count, total_questions = _score_from_answers()

    open_shell()

    render_page_header(
        eyebrow="Phase 1 — Concept Validation",
        title="Test whether the concept holds up beyond first impressions.",
        subtitle=(
            "This stage reviews local demand, competitive positioning, economic realism, "
            "system quality, and whether your assumptions remain credible under pressure."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    intro_col_1, intro_col_2, intro_col_3 = st.columns(3, gap="medium")
    with intro_col_1:
        render_card(
            label="Focus",
            title="Market credibility",
            body="Check whether the demand case is evidence-based and durable enough to support the concept.",
        )
    with intro_col_2:
        render_card(
            label="Focus",
            title="Economic realism",
            body="Pressure test revenue, costs, labor needs, and the path to acceptable performance.",
        )
    with intro_col_3:
        render_card(
            label="Focus",
            title="System quality",
            body="Assess whether the franchisor and operating model support execution in a practical way.",
        )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_core_inputs()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_live_progress(score, verdict, answered_count, total_questions)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_question_groups()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_notes()

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

    if st.button(
        "Continue to Opportunity Fit & Recommendations",
        key="phase1_continue",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["current_page"] = "Opportunity Fit & Recommendations"
        st.rerun()

    close_shell()
