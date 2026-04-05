# opportunity_fit_ui.py

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
RATING_MIN = 1
RATING_MAX = 5
DEFAULT_RATING = 3


@dataclass(frozen=True)
class FitQuestionGroup:
    title: str
    description: str
    questions: tuple[str, ...]


QUESTION_GROUPS: tuple[FitQuestionGroup, ...] = (
    FitQuestionGroup(
        title="Personal Alignment",
        description="Assess whether this opportunity fits how you actually want to work and operate.",
        questions=(
            "1. Does this opportunity match the kind of day-to-day work you want to do?",
            "2. Does the business fit the lifestyle you realistically want over the next few years?",
            "3. Does the ownership model match your preferred level of involvement?",
            "4. Are you likely to stay engaged even when the work becomes repetitive or operationally heavy?",
            "5. Does this opportunity align with your reasons for pursuing ownership in the first place?",
            "6. Would you still want this business if the brand prestige mattered less than expected?",
        ),
    ),
    FitQuestionGroup(
        title="Financial Fit",
        description="Evaluate whether the economics and exposure fit your actual financial position.",
        questions=(
            "7. Does the capital required fit your current financial reality without overreaching?",
            "8. Could you absorb a slower ramp without creating personal financial stress?",
            "9. Does the downside exposure feel acceptable relative to the upside?",
            "10. Would this still make sense if returns are more modest than the initial pitch suggests?",
            "11. Are you comfortable with the tradeoff between risk, effort, and expected return?",
            "12. Could this opportunity coexist with your other financial priorities responsibly?",
        ),
    ),
    FitQuestionGroup(
        title="Execution Fit",
        description="Check whether you can realistically execute what this business may require.",
        questions=(
            "13. Do you believe you can handle the operating rhythm this concept requires?",
            "14. Does the staffing model feel manageable given your skills and tolerance?",
            "15. Are you comfortable with the level of systems discipline this business may require?",
            "16. Could you stay steady if operations are harder than expected early on?",
            "17. Do you have enough personal bandwidth to lead through setbacks and ambiguity?",
            "18. Does the level of complexity feel justified by the opportunity?",
        ),
    ),
    FitQuestionGroup(
        title="Decision Quality",
        description="Make sure your decision is grounded in fit and evidence, not momentum.",
        questions=(
            "19. Are you making this decision from clarity rather than urgency?",
            "20. Have your biggest concerns been identified clearly rather than minimized?",
            "21. Would you feel comfortable explaining this decision to a skeptical advisor?",
            "22. Are you still willing to walk away if the fit proves weaker than hoped?",
            "23. Does the opportunity still make sense when viewed conservatively?",
            "24. Does moving forward feel earned by the evidence so far?",
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
            "Stronger opportunity fit signal",
            "The current inputs suggest the opportunity appears more aligned with your goals, constraints, and execution profile.",
        )
    if score >= 58:
        return (
            "Mixed opportunity fit signal",
            "Some elements appear to fit well, but there are still tensions that deserve closer scrutiny before confidence is warranted.",
        )
    return (
        "Weaker opportunity fit signal",
        "The current inputs suggest the opportunity may be less aligned with your actual situation than it first appears.",
    )


def _score_from_answers() -> tuple[int, str, str, list[str], list[str], int, int]:
    strengths: list[str] = []
    watchouts: list[str] = []

    alignment_score = int(st.session_state.get("of_personal_alignment_score", DEFAULT_RATING))
    financial_fit_score = int(st.session_state.get("of_financial_fit_score", DEFAULT_RATING))
    execution_fit_score = int(st.session_state.get("of_execution_fit_score", DEFAULT_RATING))
    conviction_score = int(st.session_state.get("of_decision_conviction_score", DEFAULT_RATING))
    family_support_score = int(st.session_state.get("of_support_system_score", DEFAULT_RATING))

    answer_keys = [f"of_q{i}" for i in range(1, 25)]
    values = [st.session_state.get(key, "Select one...") for key in answer_keys]
    points = [_answer_points(value) for value in values]

    answered_count = sum(1 for value in values if value != "Select one...")
    total_questions = len(answer_keys)
    total_points = sum(points)

    quality_ratio = (total_points / (answered_count * 5)) if answered_count > 0 else 0
    completion_ratio = answered_count / total_questions if total_questions else 0

    score = 20 + round(quality_ratio * 55) + round(completion_ratio * 15)

    if alignment_score >= 4:
        score += 6
        strengths.append("The opportunity appears more aligned with how you want to work and operate.")
    elif alignment_score <= 2:
        watchouts.append("There may be a meaningful gap between the business model and your preferred operating reality.")

    if financial_fit_score >= 4:
        score += 7
        strengths.append("The financial demands appear more compatible with your current situation.")
    elif financial_fit_score <= 2:
        watchouts.append("The financial exposure may be heavier than your current situation comfortably supports.")

    if execution_fit_score >= 4:
        score += 6
        strengths.append("You appear better positioned to handle the execution demands of the business.")
    elif execution_fit_score <= 2:
        watchouts.append("The practical operating demands may be harder for you to absorb consistently.")

    if conviction_score >= 4:
        score += 4
        strengths.append("Your decision posture appears more grounded and deliberate.")
    elif conviction_score <= 2:
        watchouts.append("The decision may still be carrying more uncertainty than your current conviction suggests.")

    if family_support_score >= 4:
        score += 4
        strengths.append("Your support system appears more likely to hold up under the demands of ownership.")
    elif family_support_score <= 2:
        watchouts.append("Weak support around you can make the practical burden of ownership heavier than expected.")

    if st.session_state.get("of_q8", "Somewhat") == "No":
        watchouts.append("If a slower ramp would cause personal stress, the deal deserves extra caution.")
    if st.session_state.get("of_q9", "Somewhat") == "No":
        watchouts.append("If downside exposure feels unacceptable, the opportunity may not be a good fit regardless of upside.")
    if st.session_state.get("of_q19", "Somewhat") == "No":
        watchouts.append("Urgency is often a poor foundation for a long-term ownership decision.")
    if st.session_state.get("of_q22", "Somewhat") == "No":
        watchouts.append("If you are no longer willing to walk away, discipline may be slipping.")
    if st.session_state.get("signed_anything", False):
        watchouts.append("Prior commitment can make it harder to evaluate fit objectively.")

    franchise_name = st.session_state.get("franchise_name", "").strip()
    if franchise_name:
        strengths.append(f"You are now evaluating fit with more structure rather than reacting only to the appeal of {franchise_name}.")

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
            body="A directional signal based on your present fit inputs and answers.",
        )
    with col2:
        render_card(
            label="Signal",
            title=verdict,
            body="This becomes more reliable as the full fit review is completed.",
        )
    with col3:
        render_card(
            label="Completion",
            title=f"{answered_count} of {total_questions}",
            body="Complete every section for a stronger read on actual fit.",
        )

    st.progress(progress_ratio)


def _render_core_inputs() -> None:
    render_section_intro(
        title="Core fit inputs",
        body="These higher-level inputs capture how well the opportunity fits your current reality. Keep them realistic.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.slider(
            "Personal Alignment",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("of_personal_alignment_score", DEFAULT_RATING)),
            key="of_personal_alignment_score",
            help="1 = weak fit, 5 = strong fit",
        )
        st.slider(
            "Financial Fit",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("of_financial_fit_score", DEFAULT_RATING)),
            key="of_financial_fit_score",
            help="1 = poor fit, 5 = strong fit",
        )
        st.slider(
            "Execution Fit",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("of_execution_fit_score", DEFAULT_RATING)),
            key="of_execution_fit_score",
            help="1 = weak fit, 5 = strong fit",
        )

    with col2:
        st.slider(
            "Decision Conviction",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("of_decision_conviction_score", DEFAULT_RATING)),
            key="of_decision_conviction_score",
            help="1 = low clarity, 5 = high clarity",
        )
        st.slider(
            "Support System Strength",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("of_support_system_score", DEFAULT_RATING)),
            key="of_support_system_score",
            help="1 = weak support, 5 = strong support",
        )
        st.text_input(
            "Primary Decision Driver",
            value=st.session_state.get("of_primary_driver", ""),
            key="of_primary_driver",
            placeholder="What is the main reason this opportunity still feels worth pursuing?",
        )


def _render_question_groups() -> None:
    render_section_intro(
        title="Opportunity fit questions",
        body="Answer based on what is true in your actual life and operating context. Fit matters more than excitement.",
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
                    key=f"of_q{question_number}",
                )


def _render_notes() -> None:
    render_section_intro(
        title="Fit notes",
        body="Use this space to capture where the opportunity fits well and where it still feels forced.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.text_area(
        "What looks most aligned between this opportunity and your current situation?",
        value=st.session_state.get("of_alignment_notes", ""),
        key="of_alignment_notes",
        height=100,
        placeholder="Examples: work style, financial capacity, support system, long-term goals, operating model",
    )
    st.text_area(
        "Where does the opportunity still feel stretched, forced, or uncertain?",
        value=st.session_state.get("of_tension_notes", ""),
        key="of_tension_notes",
        height=100,
        placeholder="Examples: hours, risk, staffing, family impact, capital pressure, execution complexity",
    )
    st.text_area(
        "What would need to improve for this to feel clearly right?",
        value=st.session_state.get("of_conditions_notes", ""),
        key="of_conditions_notes",
        height=100,
        placeholder="Examples: stronger economics, clearer support, better timeline, lower exposure, better location confidence",
    )


def _render_results(
    *,
    score: int,
    verdict: str,
    verdict_body: str,
    strengths: list[str],
    watchouts: list[str],
) -> None:
    st.session_state["opportunity_fit_score"] = score

    render_section_intro(
        title="Current result",
        body="Treat this as a structured fit signal. A good business can still be the wrong fit for your actual situation.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        render_card(
            label="Fit signal",
            title=verdict,
            body=verdict_body,
        )

    with col2:
        next_step = (
            "Continue to Financial Model"
            if score >= 55
            else "Continue carefully and pressure test the weaker fit areas first"
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
        title="The right opportunity still has to fit your real life.",
        body=(
            "This stage is meant to prevent a common mistake: pursuing a business that looks attractive in theory but creates strain in practice."
        ),
    )


def render_opportunity_fit() -> None:
    score, verdict, verdict_body, strengths, watchouts, answered_count, total_questions = _score_from_answers()

    open_shell()

    render_page_header(
        eyebrow="Phase 1 — Opportunity Fit & Recommendations",
        title="Decide whether this opportunity actually fits you.",
        subtitle=(
            "This stage brings together personal alignment, financial fit, execution reality, "
            "and decision quality so the opportunity can be judged against your real situation."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    intro_col_1, intro_col_2, intro_col_3 = st.columns(3, gap="medium")
    with intro_col_1:
        render_card(
            label="Focus",
            title="Personal fit",
            body="Assess whether the work, pace, and ownership reality match how you actually want to operate.",
        )
    with intro_col_2:
        render_card(
            label="Focus",
            title="Financial fit",
            body="Check whether the economics and downside exposure match your actual capacity and priorities.",
        )
    with intro_col_3:
        render_card(
            label="Focus",
            title="Decision quality",
            body="Make sure the decision is being supported by fit and evidence rather than urgency or momentum.",
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

    st.session_state["phase_2_complete"] = True

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if st.button(
        "Continue to Financial Model",
        key="opportunity_fit_continue",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["current_page"] = "Financial Model"
        st.rerun()

    close_shell()
