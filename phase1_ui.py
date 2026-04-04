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
        .cv-hero, .cv-card, .cv-featured, .cv-helper, .cv-metric, .cv-live {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            background: rgba(255,255,255,.02);
        }
        .cv-hero { padding: 1.3rem; margin-bottom: 1rem; }
        .cv-card, .cv-featured, .cv-helper, .cv-metric, .cv-live { padding: 1rem; margin-bottom: 1rem; }
        .cv-kicker { font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.06em; opacity: 0.72; margin-bottom: 0.4rem; }
        .cv-title { font-size: 1.9rem; font-weight: 700; line-height: 1.15; margin-bottom: 0.45rem; }
        .cv-subtitle { font-size: 1rem; opacity: 0.92; }
        .cv-section-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 0.35rem; }
        .cv-card-title { font-size: 1.08rem; font-weight: 700; margin-bottom: 0.2rem; }
        .cv-badge { display: inline-block; font-size: 0.74rem; font-weight: 600; padding: 0.22rem 0.5rem; border-radius: 999px; border: 1px solid rgba(120,120,120,.28); margin-bottom: 0.55rem; }
        .cv-big { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.25rem; }
        .cv-muted { opacity: 0.84; }
        .cv-metric-label { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.72; margin-bottom: 0.2rem; }
        .cv-metric-value { font-size: 1.45rem; font-weight: 700; line-height: 1.1; }
        .cv-live-title { font-size: 0.9rem; font-weight: 700; margin-bottom: 0.35rem; }

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


def _get_result_class(result: str) -> str:
    if result == "Stronger Concept Fit Signal":
        return "result-good"
    if result == "Mixed Concept Fit Signal":
        return "result-caution"
    return "result-bad"


def _get_metric_class(score: int) -> str:
    if score >= 78:
        return "metric-good"
    if score >= 58:
        return "metric-caution"
    return "metric-bad"


def _score_concept() -> tuple[int, str, list[str], list[str], int, int]:
    aligns = []
    cautions = []

    question_keys = [f"cv_q{i}" for i in range(1, 31)]
    values = [st.session_state.get(k, "Select one...") for k in question_keys]
    points = [_answer_points(v) for v in values]
    answered_count = sum(1 for v in values if v != "Select one...")
    total_questions = len(question_keys)
    total_points = sum(points)

    quality_ratio = (total_points / (answered_count * 5)) if answered_count > 0 else 0
    completion_ratio = answered_count / total_questions

    score = 20 + round(quality_ratio * 55) + round(completion_ratio * 15)

    people_score = st.session_state.get("people_management_comfort_score", 3)
    ops_score = st.session_state.get("operational_willingness_score", 3)
    structure_pref = st.session_state.get("prefers_structure_process", False)

    if ops_score >= 4:
        score += 4
        aligns.append("Your willingness to be hands-on may align better with concepts that need heavier owner involvement.")
    elif ops_score <= 2:
        cautions.append("Lower interest in daily operations may create mismatch in concepts that depend on owner effort early.")

    if people_score >= 4:
        score += 3
        aligns.append("Higher comfort with people management may help in labor-heavy or staff-intensive models.")
    elif people_score <= 2:
        cautions.append("If people management is not a strength, team-heavy concepts deserve extra caution.")

    if structure_pref:
        score += 3
        aligns.append("A preference for structure and repeatability may align better with more process-driven concepts.")

    if values[1] == "No":
        cautions.append("If you do not think the concept has repeat demand, demand stability may be weaker than the pitch suggests.")
    if values[2] == "No":
        cautions.append("If the concept is hard to differentiate locally, customer acquisition may be tougher than expected.")
    if values[3] == "No":
        cautions.append("If the model is not very repeatable, execution risk often rises.")
    if values[4] == "No":
        cautions.append("If the model relies heavily on owner involvement, the concept may fit less well for lower-touch ownership goals.")
    if values[8] == "No":
        cautions.append("A labor-heavy concept can create more operational friction than many buyers expect.")
    if values[13] == "No":
        cautions.append("Low purchase frequency can increase pressure on traffic and customer acquisition.")
    if values[19] == "No":
        cautions.append("If local demand is less resilient, the concept may be more fragile than it first appears.")

    if values[0] == "Yes":
        aligns.append("The concept appears to solve a real customer need.")
    if values[5] == "Yes":
        aligns.append("The model appears easier to explain operationally, which usually helps execution.")
    if values[6] == "Yes":
        aligns.append("A concept with clearer process discipline may be easier to manage.")
    if values[11] == "Yes":
        aligns.append("The model appears easier to train and transfer across staff.")
    if values[17] == "Yes":
        aligns.append("The concept appears more durable if local competition increases.")

    score = max(1, min(100, score))

    if score >= 78:
        result = "Stronger Concept Fit Signal"
    elif score >= 58:
        result = "Mixed Concept Fit Signal"
    else:
        result = "Weak Concept Fit Signal"

    deduped_aligns = []
    seen = set()
    for item in aligns:
        if item not in seen:
            deduped_aligns.append(item)
            seen.add(item)

    deduped_cautions = []
    seen = set()
    for item in cautions:
        if item not in seen:
            deduped_cautions.append(item)
            seen.add(item)

    return score, result, deduped_aligns[:6], deduped_cautions[:6], answered_count, total_questions


def render_phase_1():
    _inject_styles()

    st.title("Concept Validation")

    st.markdown(
        """
        <div class="cv-hero">
            <div class="cv-kicker">Phase 1 — Self & Idea</div>
            <div class="cv-title">Test whether the concept fits the work required.</div>
            <div class="cv-subtitle">
                The question is not just whether the concept sounds attractive. The question is whether the operating model,
                demand pattern, labor intensity, and owner dependency fit how you actually want to operate.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### What to Look At")
    st.write("- Demand pattern and customer behavior")
    st.write("- Operating complexity")
    st.write("- Labor intensity")
    st.write("- Repeatability of the model")
    st.write("- Owner dependency")
    st.write("- Local differentiation and resilience")

    st.markdown("### What’s Common in the Industry")
    st.write("Many concepts are easier to sell than they are to operate. Buyers often underestimate staffing pressure, execution complexity, and how much local demand really matters.")

    st.markdown("### What to Ask")
    st.write("- Does this concept solve a real, repeatable customer need?")
    st.write("- Is the model attractive because it is a good business, or because it is easy to imagine myself in it?")
    st.write("- Does this concept depend on more labor, owner effort, or local traffic than it first appears?")
    st.write("- Does the operating reality fit how I actually want to work?")

    st.markdown("### Pressure Test")
    st.write("If demand is slower, staffing is harder, and the owner has to step in more often than expected, does this still look like a fit?")

    live_score, live_result, _, _, answered_count, total_questions = _score_concept()
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
                {live_result}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)
    

    st.markdown(
    f"""
    <div class="sticky-score-wrap">
        <div class="sticky-score-inner {live_metric_class}">
            <div class="cv-live-title">Live Score Summary</div>
            <div class="cv-muted">
                Current Score: <strong>{live_score}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
                Answered: <strong>{answered_count} / {total_questions}</strong> &nbsp;&nbsp;|&nbsp;&nbsp;
                Current Signal: <strong>{live_result}</strong>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

    st.markdown("---")
    st.markdown("### 30 Concept Validation Questions")

    questions = [
        "1. Does the concept appear to solve a real customer need?",
        "2. Does the business appear to benefit from recurring or repeat customer demand?",
        "3. Does the concept appear clearly differentiated in a local market?",
        "4. Does the model appear process-driven and repeatable?",
        "5. Does the concept appear less dependent on heavy owner involvement than many early-stage businesses?",
        "6. Is the operating model relatively easy to understand at a practical level?",
        "7. Does the concept appear structured rather than chaotic?",
        "8. Does the model look easier to manage than many labor-heavy businesses?",
        "9. Does the business appear less staffing-intensive than a typical high-touch concept?",
        "10. Does the concept appear less vulnerable to constant turnover pressure?",
        "11. Does the model appear easier to oversee consistently across locations or managers?",
        "12. Does the business look trainable without needing unusually strong individual operators?",
        "13. Does the concept appear less operationally complex than it first sounds?",
        "14. Does the business seem to support frequent or repeat customer usage?",
        "15. Does the concept appear less dependent on one-time purchases or novelty traffic?",
        "16. Does the model appear to have healthier local demand durability?",
        "17. Does the business seem easier to market locally than some other concepts?",
        "18. Does the concept appear more defensible if competition increases?",
        "19. Does the model look like it can hold up if margins tighten?",
        "20. Does the business seem resilient enough if the local market softens?",
        "21. Does the concept appear less exposed to major consumer behavior swings?",
        "22. Does the operating model seem realistic rather than overly idealized?",
        "23. Does the business appear less dependent on perfect execution just to survive?",
        "24. Does the concept look like something you would still want if the first year is harder than expected?",
        "25. Does the business appear more aligned with your actual operating style?",
        "26. Does the concept appear more aligned with your people-management comfort level?",
        "27. Does the model appear to fit your time availability better than a highly intensive concept would?",
        "28. Does the concept appear more aligned with your risk tolerance?",
        "29. Does the business appear more aligned with your capital flexibility?",
        "30. Are you evaluating this concept based on business reality rather than brand excitement alone?",
    ]

    col1, col2 = st.columns(2)
    for i, question in enumerate(questions, start=1):
        with col1 if i <= 15 else col2:
            st.selectbox(question, ANSWER_OPTIONS, key=f"cv_q{i}")

    st.markdown("---")
    st.markdown("### Reflection Notes")

    st.text_area(
        "What part of the concept sounds strongest on paper?",
        value=st.session_state.get("concept_strengths_notes", ""),
        key="concept_strengths_notes",
        height=90,
        placeholder="Examples: recurring demand, simple service model, stronger differentiation, easier training, lower labor pressure",
    )

    st.text_area(
        "What part of the concept concerns you most?",
        value=st.session_state.get("concept_concerns_notes", ""),
        key="concept_concerns_notes",
        height=90,
        placeholder="Examples: staffing, owner dependency, margin pressure, weak repeat demand, competition, local awareness",
    )

    st.text_area(
        "What would need to be true for this concept to fit you well?",
        value=st.session_state.get("concept_fit_conditions_notes", ""),
        key="concept_fit_conditions_notes",
        height=90,
        placeholder="Examples: manageable staffing, stronger local demand, less owner dependency, clearer repeatability, better margins",
    )

    score, result, aligns, cautions, answered_count, total_questions = _score_concept()
    st.session_state["concept_score"] = score

    result_class = _get_result_class(result)
    metric_class = _get_metric_class(score)

    st.markdown("---")
    st.markdown(
        f"""
        <div class="cv-featured {result_class}">
            <div class="cv-badge">Current Result</div>
            <div class="cv-big">{result}</div>
            <div class="cv-muted">
                This result reflects how the concept appears to line up with your likely operating style,
                the structure of the model, and the quality of the underlying business pattern.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(
            f"""
            <div class="cv-metric {metric_class}">
                <div class="cv-metric-label">Concept Score</div>
                <div class="cv-metric-value">{score}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mc2:
        fit_signal = "Continue to Opportunity Fit" if score >= 55 else "Continue, but fit looks less clean"
        st.markdown(
            f"""
            <div class="cv-metric">
                <div class="cv-metric-label">Fit Signal</div>
                <div class="cv-metric-value" style="font-size:1.05rem;">{fit_signal}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="cv-section-title">What Appears to Align</div>', unsafe_allow_html=True)
        if aligns:
            for item in aligns:
                st.write(f"- {item}")
        else:
            st.write("- No strong alignment signals identified yet.")

    with c2:
        st.markdown('<div class="cv-section-title">What to Be Careful With</div>', unsafe_allow_html=True)
        if cautions:
            for item in cautions:
                st.write(f"- {item}")
        else:
            st.write("- No major concept watch-outs identified yet.")

    st.markdown(
        """
        <div class="cv-helper">
            <div class="cv-card-title">Industry-pattern caution</div>
            <div class="cv-muted">
                A concept can look attractive at a high level and still be a poor operating fit.
                The more the model depends on labor, constant owner attention, or strong local execution,
                the more concept fit matters.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Continue to Opportunity Fit & Recommendations", key="phase1_continue", use_container_width=True):
        st.session_state["current_page"] = "Opportunity Fit & Recommendations"
        st.rerun()
