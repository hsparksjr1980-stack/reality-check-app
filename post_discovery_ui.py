import streamlit as st


ANSWER_OPTIONS = ["Select one...", "Yes", "Somewhat", "No"]


def _sidebar_color(score: int):
    if score >= 78:
        return "#3cb371", "rgba(60,179,113,.12)"
    elif score >= 58:
        return "#ffc107", "rgba(255,193,7,.12)"
    else:
        return "#dc3545", "rgba(220,53,69,.12)"


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .pd-hero, .pd-card, .pd-featured, .pd-helper, .pd-metric, .pd-live {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            background: rgba(255,255,255,.02);
        }
        .pd-hero { padding: 1.3rem; margin-bottom: 1rem; }
        .pd-card, .pd-featured, .pd-helper, .pd-metric, .pd-live { padding: 1rem; margin-bottom: 1rem; }
        .pd-kicker { font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.06em; opacity: 0.72; margin-bottom: 0.4rem; }
        .pd-title { font-size: 1.9rem; font-weight: 700; line-height: 1.15; margin-bottom: 0.45rem; }
        .pd-subtitle { font-size: 1rem; opacity: 0.92; }
        .pd-section-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 0.35rem; }
        .pd-card-title { font-size: 1.08rem; font-weight: 700; margin-bottom: 0.2rem; }
        .pd-badge { display: inline-block; font-size: 0.74rem; font-weight: 600; padding: 0.22rem 0.5rem; border-radius: 999px; border: 1px solid rgba(120,120,120,.28); margin-bottom: 0.55rem; }
        .pd-big { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.25rem; }
        .pd-muted { opacity: 0.84; }
        .pd-metric-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.72; margin-bottom: 0.2rem; }
        .pd-metric-value { font-size: 1.45rem; font-weight: 700; line-height: 1.1; }
        .pd-live-title { font-size: 0.9rem; font-weight: 700; margin-bottom: 0.35rem; }

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
    if verdict == "Stronger Pre-Commitment Signal":
        return "result-good"
    if verdict == "Proceed with Conditions Signal":
        return "result-caution"
    return "result-bad"


def _get_metric_class(score: int) -> str:
    if score >= 78:
        return "metric-good"
    if score >= 58:
        return "metric-caution"
    return "metric-bad"


def _score_post_discovery() -> tuple[int, str, list[str], list[str], int, int]:
    positives = []
    conditions = []

    question_keys = [f"pd_q{i}" for i in range(1, 31)]
    values = [st.session_state.get(k, "Select one...") for k in question_keys]
    points = [_answer_points(v) for v in values]
    answered_count = sum(1 for v in values if v != "Select one...")
    total_questions = len(question_keys)
    total_points = sum(points)

    quality_ratio = (total_points / (answered_count * 5)) if answered_count > 0 else 0
    completion_ratio = answered_count / total_questions

    score = 20 + round(quality_ratio * 55) + round(completion_ratio * 15)

    # Key signals
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
        conditions.append("If the revenue assumptions are still not grounded, the deal remains too dependent on optimism.")
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
        conditions.append("If you still feel more emotionally committed than objectively grounded, the decision quality is weaker.")
    if values[28] == "No":
        conditions.append("If you are still not willing to walk away, negotiation leverage and discipline are reduced.")
    if values[29] == "Yes":
        positives.append("The deal appears more grounded in facts than in early excitement.")

    # Session flags for later engines
    st.session_state["flag_major_unknowns_remaining"] = values[4] == "Yes"
    st.session_state["flag_unverified_unit_economics"] = values[5] == "No"
    st.session_state["flag_no_margin_for_error"] = values[20] == "No"

    score = max(1, min(100, score))

    if score >= 78:
        verdict = "Stronger Pre-Commitment Signal"
    elif score >= 58:
        verdict = "Proceed with Conditions Signal"
    else:
        verdict = "Weak Pre-Commitment Signal"

    deduped_positives = []
    seen = set()
    for item in positives:
        if item not in seen:
            deduped_positives.append(item)
            seen.add(item)

    deduped_conditions = []
    seen = set()
    for item in conditions:
        if item not in seen:
            deduped_conditions.append(item)
            seen.add(item)

    return score, verdict, deduped_positives[:6], deduped_conditions[:6], answered_count, total_questions


def render_post_discovery():
    _inject_styles()

    st.title("Post-Discovery Review")

    st.markdown(
        """
        <div class="pd-hero">
            <div class="pd-kicker">Phase 2 — Pre-Commitment</div>
            <div class="pd-title">Review the real deal, not the early story.</div>
            <div class="pd-subtitle">
                At this stage, the goal is to pressure test what is now known, what is still unknown, and what must be true
                before a clean decision to move forward makes sense.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### What to Look At")
    st.write("- Rent and occupancy structure")
    st.write("- Buildout costs and remaining uncertainty")
    st.write("- Lease terms and commitments")
    st.write("- Financing path and liquidity pressure")
    st.write("- Unknowns that still have not become facts")
    st.write("- Whether the real deal still fits your original expectations")

    st.markdown("### What’s Common in the Industry")
    st.write("Many deals still look acceptable until real numbers, lease terms, lender expectations, and buildout realities come into view. This is where weak assumptions tend to show up.")

    st.markdown("### What to Ask")
    st.write("- What do I now know that I did not know earlier?")
    st.write("- What still remains too uncertain?")
    st.write("- What conditions must be true before this deal is worth carrying forward?")
    st.write("- Am I still relying on optimism where I should now have facts?")

    st.markdown("### Pressure Test")
    st.write("If buildout rises, rent is less favorable, ramp is slower, or lender terms tighten, does the deal still hold up?")

    live_score, live_verdict, _, _, answered_count, total_questions = _score_post_discovery()
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
        <div class="pd-live {live_metric_class}">
            <div class="pd-live-title">Live Score Summary</div>
            <div class="pd-muted">
                Current Score: <strong>{live_score}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
                Answered: <strong>{answered_count} / {total_questions}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
                Current Signal: <strong>{live_verdict}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 30 Post-Discovery Questions")

    questions = [
        "1. Are rent assumptions now grounded enough to rely on?",
        "2. Are buildout costs now materially more developed?",
        "3. Have lease terms been reviewed enough to understand real occupancy exposure?",
        "4. Is the financing path now more concrete than it was earlier?",
        "5. Are there still meaningful key unknowns remaining?",
        "6. Are revenue assumptions now grounded enough to test seriously?",
        "7. Are labor assumptions more reliable than they were earlier?",
        "8. Are vendor and supply assumptions sufficiently developed?",
        "9. Are utilities, occupancy, and fixed costs more grounded now?",
        "10. Are working capital needs clearer now than before?",
        "11. Are lender expectations and underwriting assumptions more defined now?",
        "12. Are landlord or lease negotiations grounded enough to judge the deal realistically?",
        "13. Do the site economics make more sense now than they did earlier?",
        "14. Is personal guarantee exposure more fully understood now?",
        "15. Are downside and exit scenarios clearer now than before?",
        "16. Is more of the deal now based on facts rather than sales framing?",
        "17. Does the opening path now look realistic rather than idealized?",
        "18. Is the execution burden better understood now?",
        "19. Is the actual capital requirement more grounded now?",
        "20. Have the key assumptions been pressure-tested enough to rely on?",
        "21. Does the deal still work if things do not go perfectly?",
        "22. Is cost overrun risk now bounded enough to be acceptable?",
        "23. Is ramp timing realistic enough to support a decision?",
        "24. Is staffing readiness clearer now than it was before?",
        "25. Is local market demand convincing enough to support the assumptions?",
        "26. Does the actual deal still fit your operating reality?",
        "27. Are your conditions for moving forward clearly defined now?",
        "28. Do you feel more objectively grounded than emotionally committed at this point?",
        "29. Are you still willing to walk away if the conditions do not hold up?",
        "30. Is the deal now more grounded in facts than in early excitement?",
    ]

    col1, col2 = st.columns(2)
    for i, question in enumerate(questions, start=1):
        with col1 if i <= 15 else col2:
            st.selectbox(question, ANSWER_OPTIONS, key=f"pd_q{i}")

    st.markdown("---")
    st.markdown("### Reflection Notes")

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

    score, verdict, positives, conditions, answered_count, total_questions = _score_post_discovery()
    st.session_state["post_discovery_score"] = score

    result_class = _get_result_class(verdict)
    metric_class = _get_metric_class(score)

    st.markdown("---")
    st.markdown(
        f"""
        <div class="pd-featured {result_class}">
            <div class="pd-badge">Current Result</div>
            <div class="pd-big">{verdict}</div>
            <div class="pd-muted">
                This result reflects how much of the deal now appears grounded versus how much still depends on unresolved facts or conditions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(
            f"""
            <div class="pd-metric {metric_class}">
                <div class="pd-metric-label">Post-Discovery Score</div>
                <div class="pd-metric-value">{score}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mc2:
        signal = "Cleaner" if score >= 78 else "Conditional" if score >= 58 else "Weak"
        st.markdown(
            f"""
            <div class="pd-metric">
                <div class="pd-metric-label">Decision Signal</div>
                <div class="pd-metric-value" style="font-size:1.05rem;">{signal}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="pd-section-title">What Looks More Grounded</div>', unsafe_allow_html=True)
        if positives:
            for item in positives:
                st.write(f"- {item}")
        else:
            st.write("- Few elements look fully grounded yet.")

    with c2:
        st.markdown('<div class="pd-section-title">Conditions Before Proceeding</div>', unsafe_allow_html=True)
        if conditions:
            for item in conditions:
                st.write(f"- {item}")
        else:
            st.write("- No major open conditions identified yet.")

    st.markdown(
        """
        <div class="pd-helper">
            <div class="pd-card-title">How to use this result</div>
            <div class="pd-muted">
                This stage is about deciding whether the remaining unknowns are acceptable, fixable, or too meaningful to ignore.
                A deal does not need to be perfect, but it should become more grounded as discovery progresses.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Continue to Final Decision", key="post_discovery_continue", use_container_width=True):
        st.session_state["current_page"] = "Final Decision"
        st.rerun()
