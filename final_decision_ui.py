# final_decision_ui.py

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
class DecisionQuestionGroup:
    title: str
    description: str
    questions: tuple[str, ...]


QUESTION_GROUPS: tuple[DecisionQuestionGroup, ...] = (
    DecisionQuestionGroup(
        title="Deal Quality",
        description="Confirm whether the actual opportunity now looks credible enough to justify action.",
        questions=(
            "1. Does the opportunity still look credible after the work completed so far?",
            "2. Do the current economics appear realistic enough to support a decision?",
            "3. Are the biggest unknowns now narrow enough to be acceptable?",
            "4. Does the downside exposure feel proportionate to the upside?",
            "5. Would you still pursue this deal if outcomes are more modest than hoped?",
            "6. Does the actual deal still look stronger than the early pitch alone?",
        ),
    ),
    DecisionQuestionGroup(
        title="Personal and Financial Readiness",
        description="Assess whether you are truly ready to carry the reality of the deal forward.",
        questions=(
            "7. Does this opportunity still fit your actual operating reality?",
            "8. Are you financially positioned to absorb a slower or harder start if needed?",
            "9. Is your support system strong enough for the practical demands ahead?",
            "10. Are you still comfortable with the level of time and stress this may require?",
            "11. Are you prepared to lead through ambiguity and setbacks early on?",
            "12. Does moving forward still fit your broader priorities responsibly?",
        ),
    ),
    DecisionQuestionGroup(
        title="Conditions and Discipline",
        description="Make sure the decision is anchored in conditions, not momentum or sunk cost.",
        questions=(
            "13. Have you clearly defined what must be true before you commit?",
            "14. Are the remaining open items specific enough to negotiate or verify?",
            "15. Are you making this decision from clarity rather than urgency?",
            "16. Would you still be comfortable defending this decision to a skeptical advisor?",
            "17. Are you still willing to walk away if key conditions fail?",
            "18. Do you believe the decision has been earned by the evidence so far?",
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
        return "Conditional"
    return "Weak"


def _current_decision() -> str:
    if st.session_state.get("move_forward", False):
        return "Move Forward"
    if st.session_state.get("walk_away", False):
        return "Walk Away"
    return "No decision selected"


def _result_summary(score: int, selected_decision: str) -> tuple[str, str]:
    if selected_decision == "Walk Away":
        return (
            "Walk away",
            "Your current inputs suggest the opportunity does not justify moving forward on acceptable terms.",
        )
    if selected_decision == "Move Forward":
        return (
            "Move forward carefully",
            "The current inputs support moving forward, but only with continued discipline and attention to the remaining risks.",
        )

    if score >= 78:
        return (
            "Stronger decision signal",
            "The work completed so far supports a stronger case for moving forward carefully.",
        )
    if score >= 58:
        return (
            "Conditional decision signal",
            "The decision may still be viable, but only if the remaining issues are handled with discipline.",
        )
    return (
        "Weak decision signal",
        "The current inputs suggest more unresolved tension than a clean commitment should carry.",
    )


def _score_from_answers() -> tuple[int, str, str, list[str], list[str], int, int]:
    positives: list[str] = []
    conditions: list[str] = []

    conviction_score = int(st.session_state.get("fd_conviction_score", DEFAULT_RATING))
    readiness_score = int(st.session_state.get("fd_readiness_score", DEFAULT_RATING))
    support_score = int(st.session_state.get("fd_support_score", DEFAULT_RATING))
    risk_acceptance_score = int(st.session_state.get("fd_risk_acceptance_score", DEFAULT_RATING))
    discipline_score = int(st.session_state.get("fd_discipline_score", DEFAULT_RATING))
    selected_decision = _current_decision()

    answer_keys = [f"fd_q{i}" for i in range(1, 19)]
    values = [st.session_state.get(key, "Select one...") for key in answer_keys]
    points = [_answer_points(value) for value in values]

    answered_count = sum(1 for value in values if value != "Select one...")
    total_questions = len(answer_keys)

    quality_ratio = (sum(points) / (answered_count * 5)) if answered_count > 0 else 0
    completion_ratio = answered_count / total_questions if total_questions else 0

    score = 20 + round(quality_ratio * 55) + round(completion_ratio * 15)

    if conviction_score >= 4:
        score += 5
        positives.append("Your current conviction appears more grounded in the work completed so far.")
    elif conviction_score <= 2:
        conditions.append("Your current conviction may still be too weak for a clean commitment.")

    if readiness_score >= 4:
        score += 6
        positives.append("You appear more practically ready for the next stage of ownership.")
    elif readiness_score <= 2:
        conditions.append("Your current readiness may still be too thin for the demands ahead.")

    if support_score >= 4:
        score += 4
        positives.append("Your support system appears more likely to hold up under pressure.")
    elif support_score <= 2:
        conditions.append("Weak support around you can make a difficult deal much harder to carry.")

    if risk_acceptance_score >= 4:
        score += 5
        positives.append("The current risk profile appears more acceptable relative to the upside.")
    elif risk_acceptance_score <= 2:
        conditions.append("If the downside still feels unacceptable, the deal may not be worth carrying forward.")

    if discipline_score >= 4:
        score += 4
        positives.append("Your decision posture appears more disciplined and evidence-based.")
    elif discipline_score <= 2:
        conditions.append("The decision may still be too exposed to urgency, emotion, or sunk cost.")

    if values[2] == "No":
        conditions.append("If major unknowns are still too wide, the deal is not ready for a clean commitment.")
    if values[7] == "No":
        conditions.append("If a slower or harder start would strain you financially, the deal deserves extra caution.")
    if values[12] == "No":
        conditions.append("If your conditions for moving forward are not clearly defined, decision quality remains weaker.")
    if values[14] == "No":
        conditions.append("Urgency is a poor basis for a long-term ownership decision.")
    if values[16] == "No":
        conditions.append("If you are no longer willing to walk away, discipline and leverage both weaken.")
    if values[17] == "Yes":
        positives.append("The decision appears more earned by evidence rather than by momentum alone.")

    phase0 = st.session_state.get("readiness_score")
    phase1 = st.session_state.get("concept_validation_score")
    phase2 = st.session_state.get("post_discovery_score")
    financial = st.session_state.get("financial_score")

    prior_scores = [score for score in (phase0, phase1, phase2, financial) if isinstance(score, (int, float))]
    if prior_scores:
        avg_prior_score = sum(prior_scores) / len(prior_scores)
        if avg_prior_score >= 70:
            positives.append("Your earlier work appears broadly supportive of moving forward carefully.")
            score += 4
        elif avg_prior_score < 55:
            conditions.append("Earlier assessment work still points to meaningful friction or weak areas.")
            score -= 4

    if selected_decision == "Move Forward":
        score += 3
    elif selected_decision == "Walk Away":
        score -= 5

    score = max(1, min(100, score))
    verdict, verdict_body = _result_summary(score, selected_decision)

    deduped_positives: list[str] = []
    seen_positives: set[str] = set()
    for item in positives:
        if item not in seen_positives:
            deduped_positives.append(item)
            seen_positives.add(item)

    deduped_conditions: list[str] = []
    seen_conditions: set[str] = set()
    for item in conditions:
        if item not in seen_conditions:
            deduped_conditions.append(item)
            seen_conditions.add(item)

    return (
        score,
        verdict,
        verdict_body,
        deduped_positives[:6],
        deduped_conditions[:6],
        answered_count,
        total_questions,
    )


def _set_decision(decision: str) -> None:
    is_move_forward = decision == "Move Forward"
    is_walk_away = decision == "Walk Away"

    st.session_state["move_forward"] = is_move_forward
    st.session_state["walk_away"] = is_walk_away
    st.session_state["final_decision_submitted"] = True
    st.session_state["phase_3_complete"] = True

    if is_move_forward:
        st.session_state["premium_access"] = True

    st.session_state["current_page"] = "Report"
    st.rerun()


def _render_live_progress(score: int, verdict: str, answered_count: int, total_questions: int) -> None:
    progress_ratio = answered_count / total_questions if total_questions else 0

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        render_card(
            label="Current score",
            title=str(score),
            body="A directional signal based on your final decision inputs and prior work.",
        )
    with col2:
        render_card(
            label="Signal",
            title=verdict,
            body="This becomes more reliable as the remaining questions are completed.",
        )
    with col3:
        render_card(
            label="Completion",
            title=f"{answered_count} of {total_questions}",
            body="Finish all sections for a cleaner final read.",
        )

    st.progress(progress_ratio)


def _render_focus_cards() -> None:
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        render_card(
            label="Focus",
            title="Judge the actual deal",
            body="Base the decision on the real terms, economics, and risk exposure, not the early story.",
        )
    with col2:
        render_card(
            label="Focus",
            title="Protect decision quality",
            body="Define conditions clearly so the choice is anchored in discipline rather than momentum.",
        )
    with col3:
        render_card(
            label="Focus",
            title="Match reality",
            body="Make sure the opportunity still fits your actual operating and financial situation.",
        )


def _render_core_inputs() -> None:
    render_section_intro(
        title="Core decision inputs",
        body="These inputs capture your current level of readiness and conviction. Keep them grounded in what is true now.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.slider(
            "Decision Conviction",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("fd_conviction_score", DEFAULT_RATING)),
            key="fd_conviction_score",
            help="1 = low clarity, 5 = high clarity",
        )
        st.slider(
            "Practical Readiness",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("fd_readiness_score", DEFAULT_RATING)),
            key="fd_readiness_score",
            help="1 = weak readiness, 5 = strong readiness",
        )
        st.slider(
            "Support System Strength",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("fd_support_score", DEFAULT_RATING)),
            key="fd_support_score",
            help="1 = weak support, 5 = strong support",
        )

    with col2:
        st.slider(
            "Risk Acceptance",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("fd_risk_acceptance_score", DEFAULT_RATING)),
            key="fd_risk_acceptance_score",
            help="1 = unacceptable risk, 5 = acceptable risk",
        )
        st.slider(
            "Decision Discipline",
            min_value=RATING_MIN,
            max_value=RATING_MAX,
            value=int(st.session_state.get("fd_discipline_score", DEFAULT_RATING)),
            key="fd_discipline_score",
            help="1 = weak discipline, 5 = strong discipline",
        )

    st.caption(f"Selected decision: {_current_decision()}")


def _render_question_groups() -> None:
    render_section_intro(
        title="Final decision questions",
        body="Answer based on what the actual opportunity now looks like, not what you hoped it might become.",
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
                    key=f"fd_q{question_number}",
                )


def _render_notes() -> None:
    render_section_intro(
        title="Decision notes",
        body="Capture why you would move forward, what still has to be true, and what could still stop the deal.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.text_area(
        "What are the strongest reasons to move forward?",
        value=st.session_state.get("fd_reasons_to_proceed", ""),
        key="fd_reasons_to_proceed",
        height=100,
        placeholder="Examples: stronger economics, better fit, clearer financing, acceptable downside, stronger conviction",
    )
    st.text_area(
        "What conditions still must be true before you would commit?",
        value=st.session_state.get("fd_required_conditions", ""),
        key="fd_required_conditions",
        height=100,
        placeholder="Examples: lease threshold, buildout cap, lender clarity, support commitments, verified assumptions",
    )
    st.text_area(
        "What are the strongest reasons to walk away?",
        value=st.session_state.get("fd_reasons_to_stop", ""),
        key="fd_reasons_to_stop",
        height=100,
        placeholder="Examples: weak margin for error, poor fit, too much exposure, unresolved unknowns, thin support",
    )


def _persist_decision_outputs(score: int) -> None:
    selected_decision = _current_decision()
    st.session_state["final_decision_score"] = score
    st.session_state["phase_3_complete"] = True
    st.session_state["final_decision_submitted"] = selected_decision in {
        "Move Forward",
        "Walk Away",
    }


def _render_results(
    *,
    score: int,
    verdict: str,
    verdict_body: str,
    positives: list[str],
    conditions: list[str],
) -> None:
    _persist_decision_outputs(score)

    render_section_intro(
        title="Current result",
        body="Use this output to clarify your final posture. A strong opportunity should still survive disciplined skepticism.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        render_card(
            label="Decision signal",
            title=verdict,
            body=verdict_body,
        )

    with col2:
        selected_decision = _current_decision()
        next_step = "Select your final decision"
        if selected_decision == "Move Forward":
            next_step = "Proceed to the report, then continue into the deal workspace"
        elif selected_decision == "Walk Away":
            next_step = "Proceed to the report and close the evaluation cleanly"

        render_card(
            label="Next step",
            title=next_step,
            body=f"Current status: {_status_label(score)}.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("### Reasons supporting the decision")
        if positives:
            for item in positives:
                st.write(f"- {item}")
        else:
            st.write("- Few strong supporting reasons identified yet.")

    with c2:
        st.markdown("### Conditions and cautions")
        if conditions:
            for item in conditions:
                st.write(f"- {item}")
        else:
            st.write("- No major conditions or cautions identified yet.")

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    render_card(
        label="Decision discipline",
        title="Clarity matters more than momentum.",
        body="The best final decision is one you can explain clearly, defend conservatively, and live with under less favorable conditions.",
    )


def _render_decision_actions() -> None:
    render_section_intro(
        title="Final decision",
        body="After reviewing the full evaluation, choose the outcome that best reflects your actual decision.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    button_col_1, button_col_2 = st.columns(2, gap="large")

    with button_col_1:
        if st.button(
            "Yes, I am proceeding",
            key="fd_yes_proceeding",
            use_container_width=True,
            type="primary",
        ):
            _set_decision("Move Forward")

    with button_col_2:
        if st.button(
            "No, I am walking away",
            key="fd_no_walking_away",
            use_container_width=True,
        ):
            _set_decision("Walk Away")

    st.caption(f"Selected decision: {_current_decision()}")


def render_final_decision() -> None:
    score, verdict, verdict_body, positives, conditions, answered_count, total_questions = _score_from_answers()

    open_shell()

    render_page_header(
        eyebrow="Phase 3 — Final Decision",
        title="Decide what to do with the opportunity now.",
        subtitle=(
            "This stage brings the work together so you can decide whether to move forward "
            "or walk away with discipline."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_focus_cards()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_core_inputs()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_live_progress(score, verdict, answered_count, total_questions)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_question_groups()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_notes()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    score, verdict, verdict_body, positives, conditions, answered_count, total_questions = _score_from_answers()
    _render_results(
        score=score,
        verdict=verdict,
        verdict_body=verdict_body,
        positives=positives,
        conditions=conditions,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_decision_actions()

    close_shell()
