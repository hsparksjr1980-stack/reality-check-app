# post_discovery_ui.py

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
        title="Occupancy, Lease, and Buildout",
        description="Confirm whether the real estate and buildout assumptions now hold up under closer review.",
        questions=(
            "1. Are rent assumptions now grounded enough to rely on?",
            "2. Are buildout costs now materially more developed?",
            "3. Have lease terms been reviewed enough to understand real occupancy exposure?",
            "4. Is the financing path now more concrete than it was earlier?",
            "5. Are there still meaningful key unknowns remaining?",
            "6. Are revenue assumptions now grounded enough to test seriously?",
        ),
    ),
    QuestionGroup(
        title="Operating Assumptions",
        description="Assess whether the unit-level assumptions are becoming more factual and less optimistic.",
        questions=(
            "7. Are labor assumptions more reliable than they were earlier?",
            "8. Are vendor and supply assumptions sufficiently developed?",
            "9. Are utilities, occupancy, and fixed costs more grounded now?",
            "10. Are working capital needs clearer now than before?",
            "11. Are lender expectations and underwriting assumptions more defined now?",
            "12. Are landlord or lease negotiations grounded enough to judge the deal realistically?",
        ),
    ),
    QuestionGroup(
        title="Economics and Risk Exposure",
        description="Check whether the economics, downside exposure, and personal obligations are now clearer.",
        questions=(
            "13. Do the site economics make more sense now than they did earlier?",
            "14. Is personal guarantee exposure more fully understood now?",
            "15. Are downside and exit scenarios clearer now than before?",
            "16. Is more of the deal now based on facts rather than sales framing?",
            "17. Does the opening path now look realistic rather than idealized?",
            "18. Is the execution burden better understood now?",
        ),
    ),
    QuestionGroup(
        title="Pressure Testing",
        description="Evaluate whether the deal still works when conditions become less favorable.",
        questions=(
            "19. Is the actual capital requirement more grounded now?",
            "20. Have the key assumptions been pressure-tested enough to rely on?",
            "21. Does the deal still work if things do not go perfectly?",
            "22. Is cost overrun risk now bounded enough to be acceptable?",
            "23. Is ramp timing realistic enough to support a decision?",
            "24. Is staffing readiness clearer now than it was before?",
        ),
    ),
    QuestionGroup(
        title="Decision Readiness",
        description="Decide whether the actual deal is now grounded enough to carry forward responsibly.",
        questions=(
            "25. Is local market demand convincing enough to support the assumptions?",
            "26. Does the actual deal still fit your operating reality?",
            "27. Are your conditions for moving forward clearly defined now?",
            "28. Do you feel more objectively grounded than emotionally committed at this point?",
            "29. Are you still willing to walk away if the conditions do not hold up?",
            "30. Is the deal now more grounded in facts than in early excitement?",
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
        return "Cleaner"
    if score >= 58:
        return "Conditional"
    return "Weak"


def _result_summary(score: int) -> tuple[str, str]:
    if score >= 78:
        return (
            "Stronger pre-commitment signal",
            "More of the deal now appears grounded in facts, clearer economics, and better-defined conditions.",
        )
    if score >= 58:
        return (
            "Proceed with conditions signal",
            "Some parts of the deal appear stronger, but several conditions still need to be resolved before confidence is justified.",
        )
    return (
        "Weak pre-commitment signal",
        "Too much of the deal may still depend on unresolved facts, optimistic assumptions, or conditions that are not yet reliable.",
    )


def _score_post_discovery() -> tuple[int, str, str, list[str], list[str], int, int]:
    positives: list[str] = []
    conditions: list[str] = []

    question_keys = [f"pd_q{i}" for i in range(1, 31)]
    values = [st.session_state.get(key, "Select one...") for key in question_keys]
    points = [_answer_points(value) for value in values]

    answered_count = sum(1 for value in values if value != "Select one...")
    total_questions = len(question_keys)
    total_points = sum(points)

    quality_ratio = (total_points / (answered_count * 5)) if answered_count > 0 else 0
    completion_ratio = answered_count / total_questions if total_questions else 0

    score = 20 + round(quality_ratio * 55) + round(completion_ratio * 15)

    if values[0] == "Yes":
        positives.append("Rent assumptions appear more grounded.")
    elif values[0] == "No":
        conditions.append("Rent is still not clear enough to support a cleaner decision.")

    if values[1] == "Yes":
        positives.append("Buildout assumptions appear more developed.")
    elif values[1] == "No":
        conditions.append("Buildout costs still appear too uncertain.")

    if values[2] == "Yes":
        positives.append("Lease terms appear more in view.")
    elif values[2] == "No":
        conditions.append("Lease terms still need more pressure testing.")

    if values[3] == "Yes":
        positives.append("The financing path appears more defined.")
    elif values[3] == "No":
        conditions.append("The financing path still needs to become more concrete.")

    if values[4] == "No":
        positives.append("The number of major unknowns appears lower.")
    elif values[4] == "Yes":
        conditions.append("There are still meaningful unknowns remaining.")

    if values[5] == "No":
        conditions.append("If revenue assumptions are still not grounded, the deal remains too dependent on optimism.")
    if values[6] == "No":
        conditions.append("If labor assumptions are still unclear, operating pressure may still be understated.")
    if values[7] == "No":
        conditions.append("If vendor or supply assumptions are unresolved, execution risk remains high.")
    if values[8] == "No":
        conditions.append("If utility, occupancy, or fixed cost assumptions are still moving, downside risk remains.")
    if values[9] == "No":
        conditions.append("If working capital needs are not clearer now, liquidity pressure may still be underestimated.")
    if values[10] == "No":
        conditions.append("If lender expectations are still unclear, financing certainty is weaker than it should be by this stage.")
    if values[11] == "No":
        conditions.append("If landlord or lease negotiations are still loose, occupancy risk remains meaningful.")
    if values[12] == "No":
        conditions.append("If the site economics still do not make sense, the deal may still be weak at the unit level.")
    if values[13] == "No":
        conditions.append("If personal guarantee exposure is still not fully understood, risk remains understated.")
    if values[14] == "No":
        conditions.append("If exit or downside scenarios are still vague, the decision is less grounded than it should be.")

    if values[15] == "Yes":
        positives.append("More of the deal appears based on facts rather than sales framing.")
    if values[16] == "Yes":
        positives.append("The opening path appears more realistic.")
    if values[17] == "Yes":
        positives.append("The execution burden appears better understood.")
    if values[18] == "Yes":
        positives.append("The capital requirement appears more grounded.")
    if values[19] == "Yes":
        positives.append("The key assumptions look more pressure-tested.")
    if values[20] == "No":
        conditions.append("If the deal still requires everything to go right, the margin for error may be too thin.")
    if values[21] == "No":
        conditions.append("If cost overrun risk still feels open-ended, the deal remains fragile.")
    if values[22] == "No":
        conditions.append("If ramp timing still feels uncertain, the deal may remain too sensitive to slower performance.")
    if values[23] == "No":
        conditions.append("If staffing readiness is still unclear, opening and early operations may still be under pressure.")
    if values[24] == "No":
        conditions.append("If local market demand is still not convincing, revenue assumptions remain exposed.")
    if values[25] == "No":
        conditions.append("If the actual deal still does not fit your operating reality, moving forward may create avoidable friction.")
    if values[26] == "No":
        conditions.append("If your conditions for moving forward are still not clearly defined, discipline is weaker than it should be.")
    if values[27] == "No":
        conditions.append("If you still feel more emotionally committed than objectively grounded, decision quality is weaker.")
    if values[28] == "No":
        conditions.append("If you are still not willing to walk away, negotiation leverage and discipline are reduced.")
    if values[29] == "Yes":
        positives.append("The deal appears more grounded in facts than in early excitement.")

    st.session_state["flag_major_unknowns_remaining"] = values[4] == "Yes"
    st.session_state["flag_unverified_unit_economics"] = values[5] == "No"
    st.session_state["flag_no_margin_for_error"] = values[20] == "No"

    score = max(1, min(100, score))
    verdict, verdict_body = _result_summary(score)

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


def _render_live_progress(score: int, verdict: str, answered_count: int, total_questions: int) -> None:
    progress_ratio = answered_count / total_questions if total_questions else 0

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        render_card(
            label="Current score",
            title=str(score),
            body="A directional signal based on how much of the deal now appears grounded.",
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
            body="Complete every section for a stronger pre-commitment read.",
        )

    st.progress(progress_ratio)


def _render_focus_cards() -> None:
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        render_card(
            label="Focus",
            title="Ground the economics",
            body="Verify rent, buildout, capital needs, and margin for error against the real deal terms.",
        )

    with col2:
        render_card(
            label="Focus",
            title="Reduce unknowns",
            body="Separate what is now fact from what is still open, unresolved, or too dependent on optimism.",
        )

    with col3:
        render_card(
            label="Focus",
            title="Define conditions",
            body="Clarify what must be true before moving forward is justified on disciplined terms.",
        )


def _render_question_groups() -> None:
    render_section_intro(
        title="Post-discovery questions",
        body="Answer based on what is now known from discovery, lease review, lender conversations, and real operating assumptions.",
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
                    key=f"pd_q{question_number}",
                )


def _render_notes() -> None:
    render_section_intro(
        title="Reflection notes",
        body="Capture what is now stronger, what still concerns you, and what conditions must be true before moving forward.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    st.text_area(
        "What looks more grounded now than it did earlier?",
        value=st.session_state.get("pd_grounded_notes", ""),
        key="pd_grounded_notes",
        height=90,
        placeholder="Examples: clearer buildout, more realistic rent, lender path, better understanding of operating burden",
    )

    st.text_area(
        "What still concerns you most at this stage?",
        value=st.session_state.get("pd_biggest_concern", ""),
        key="pd_biggest_concern",
        height=90,
        placeholder="Examples: unknowns, cost overruns, weak site economics, thin margin for error, lease risk",
    )

    st.text_area(
        "What must be true before you would feel comfortable moving forward?",
        value=st.session_state.get("pd_conditions_notes", ""),
        key="pd_conditions_notes",
        height=90,
        placeholder="Examples: rent below threshold, buildout within budget, stronger lender clarity, fewer unknowns, better downside case",
    )


def _render_results(
    *,
    score: int,
    verdict: str,
    verdict_body: str,
    positives: list[str],
    conditions: list[str],
) -> None:
    st.session_state["post_discovery_score"] = score

    render_section_intro(
        title="Current result",
        body="This stage is about whether the remaining unknowns are acceptable, fixable, or too meaningful to ignore.",
    )
    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        render_card(
            label="Pre-commitment signal",
            title=verdict,
            body=verdict_body,
        )

    with col2:
        render_card(
            label="Decision posture",
            title=_status_label(score),
            body="A deal does not need to be perfect, but it should become more grounded as discovery progresses.",
        )

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("### What looks more grounded")
        if positives:
            for item in positives:
                st.write(f"- {item}")
        else:
            st.write("- Few elements look fully grounded yet.")

    with c2:
        st.markdown("### Conditions before proceeding")
        if conditions:
            for item in conditions:
                st.write(f"- {item}")
        else:
            st.write("- No major open conditions identified yet.")

    st.markdown('<div class="rc-gap-md"></div>', unsafe_allow_html=True)

    render_card(
        label="How to use this result",
        title="Judge the actual deal, not the earlier story.",
        body="The right question now is whether the remaining uncertainty is acceptable and whether the real terms still support the decision.",
    )


def render_post_discovery() -> None:
    score, verdict, verdict_body, positives, conditions, answered_count, total_questions = _score_post_discovery()

    open_shell()

    render_page_header(
        eyebrow="Phase 2 — Pre-Commitment",
        title="Review the real deal, not the early story.",
        subtitle=(
            "At this stage, the goal is to pressure test what is now known, what is still unknown, "
            "and what must be true before a clean decision to move forward makes sense."
        ),
        wide=True,
    )

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_focus_cards()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_live_progress(score, verdict, answered_count, total_questions)

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_question_groups()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    _render_notes()

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    score, verdict, verdict_body, positives, conditions, answered_count, total_questions = _score_post_discovery()
    _render_results(
        score=score,
        verdict=verdict,
        verdict_body=verdict_body,
        positives=positives,
        conditions=conditions,
    )

    st.session_state["phase_2_complete"] = True

    st.markdown('<div class="rc-gap-lg"></div>', unsafe_allow_html=True)

    if st.button(
        "Continue to Final Decision",
        key="post_discovery_continue",
        use_container_width=True,
        type="primary",
    ):
        st.session_state["current_page"] = "Final Decision"
        st.rerun()

    close_shell()
