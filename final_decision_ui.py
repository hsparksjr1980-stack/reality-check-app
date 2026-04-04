import streamlit as st
from decision_engine import build_decision_packet


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .fd-hero, .fd-card, .fd-featured, .fd-helper, .fd-metric {
            border: 1px solid rgba(120,120,120,.22);
            border-radius: 18px;
            background: rgba(255,255,255,.02);
        }
        .fd-hero { padding: 1.3rem; margin-bottom: 1rem; }
        .fd-card, .fd-featured, .fd-helper, .fd-metric { padding: 1rem; margin-bottom: 1rem; }

        .fd-kicker {
            font-size: 0.82rem;
            text-transform: uppercase;
            opacity: 0.72;
            margin-bottom: 0.4rem;
        }
        .fd-title {
            font-size: 1.9rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }
        .fd-subtitle {
            font-size: 1rem;
            opacity: 0.9;
        }

        .fd-big {
            font-size: 1.5rem;
            font-weight: 700;
        }

        .fd-metric-label {
            font-size: 0.75rem;
            opacity: 0.7;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }
        .fd-metric-value {
            font-size: 1.3rem;
            font-weight: 700;
        }

        .metric-good {
            border: 1px solid rgba(60,179,113,.4) !important;
            background: rgba(60,179,113,.1) !important;
        }
        .metric-caution {
            border: 1px solid rgba(255,193,7,.4) !important;
            background: rgba(255,193,7,.1) !important;
        }
        .metric-bad {
            border: 1px solid rgba(220,53,69,.4) !important;
            background: rgba(220,53,69,.1) !important;
        }

        .result-good {
            border: 1px solid rgba(60,179,113,.45) !important;
            background: rgba(60,179,113,.12) !important;
        }
        .result-caution {
            border: 1px solid rgba(255,193,7,.45) !important;
            background: rgba(255,193,7,.12) !important;
        }
        .result-bad {
            border: 1px solid rgba(220,53,69,.45) !important;
            background: rgba(220,53,69,.12) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _metric_class(score: float | int | None) -> str:
    if score is None:
        return ""
    if score >= 78:
        return "metric-good"
    elif score >= 58:
        return "metric-caution"
    return "metric-bad"


def _result_class(score: float | int | None) -> str:
    if score is None:
        return ""
    if score >= 78:
        return "result-good"
    elif score >= 58:
        return "result-caution"
    return "result-bad"


def _safe_score(value):
    return None if value is None else float(value)


def _build_high_level_strengths(
    readiness: float | None,
    concept: float | None,
    financial: float | None,
    post: float | None,
    pressure: float | None,
    packet: dict,
) -> list[str]:
    strengths = []

    if readiness is not None and readiness >= 78:
        strengths.append("Your Reality Check score suggests stronger readiness for the ownership and operating demands.")
    elif readiness is not None and readiness >= 58:
        strengths.append("Your Reality Check score suggests some readiness strengths, but not without friction.")

    if concept is not None and concept >= 78:
        strengths.append("Your Concept Validation score suggests the business model appears to align more cleanly with your profile.")
    elif concept is not None and concept >= 58:
        strengths.append("Your Concept Validation score suggests the concept may fit, but not without some mismatch risk.")

    if financial is not None and financial >= 78:
        strengths.append("Your Financial Model score suggests the deal can work with a healthier margin for error.")
    elif financial is not None and financial >= 58:
        strengths.append("Your Financial Model score suggests the numbers may work, but with tighter financial tolerance.")

    if post is not None and post >= 78:
        strengths.append("Your Post-Discovery score suggests more of the deal is grounded in facts rather than early assumptions.")
    elif post is not None and post >= 58:
        strengths.append("Your Post-Discovery score suggests the deal may still work, but only with conditions and more discipline.")

    if pressure is not None and pressure >= 78:
        strengths.append("Your Pressure Test score suggests the deal holds up reasonably well when assumptions are stressed.")
    elif pressure is not None and pressure >= 58:
        strengths.append("Your Pressure Test score suggests the deal may survive pressure, but with less room for error.")

    # allow engine-provided strengths if they exist
    for item in packet.get("strengths", []):
        if item not in strengths:
            strengths.append(item)

    return strengths[:6]


def _build_high_level_risks(
    readiness: float | None,
    concept: float | None,
    financial: float | None,
    post: float | None,
    pressure: float | None,
    packet: dict,
) -> list[str]:
    risks = []

    if readiness is not None and readiness < 58:
        risks.append("Your Reality Check score suggests the ownership, time, or risk profile may not align cleanly with the business demands.")

    if concept is not None and concept < 58:
        risks.append("Your Concept Validation score suggests the concept may not fit your operating style or the business pattern may be weaker than it first appears.")

    if financial is not None and financial < 58:
        risks.append("Your Financial Model score suggests the deal may not work well enough financially under the current assumptions.")

    if post is not None and post < 58:
        risks.append("Your Post-Discovery score suggests too much of the deal still depends on unresolved facts, unknowns, or weak conditions.")

    if pressure is not None and pressure < 58:
        risks.append("Your Pressure Test score suggests the deal may break down when assumptions are stressed or execution gets harder.")

    for item in packet.get("key_risks", []):
        if item not in risks:
            risks.append(item)

    for item in packet.get("conditions", []):
        if item not in risks:
            risks.append(item)

    for item in packet.get("risks", []):
        if item not in risks:
            risks.append(item)

    return risks[:8]


def render_final_decision():
    _inject_styles()

    packet = build_decision_packet()

    readiness = _safe_score(st.session_state.get("readiness_score"))
    concept = _safe_score(st.session_state.get("concept_score"))
    financial = _safe_score(st.session_state.get("financial_score"))
    post = _safe_score(st.session_state.get("post_discovery_score"))
    pressure = _safe_score(st.session_state.get("pressure_test_score"))

    overall = _safe_score(
        packet.get("final_score", packet.get("weighted_score", 0))
    )

    verdict = packet.get(
        "master_verdict",
        packet.get("recommendation", "Decision Summary")
    )

    st.title("Final Decision")

    st.markdown(
        """
        <div class="fd-hero">
            <div class="fd-kicker">Phase 3 — Decision</div>
            <div class="fd-title">Pull everything together before committing.</div>
            <div class="fd-subtitle">
                This is where you step back and evaluate the full picture —
                your fit, the concept, the financials, and the actual deal.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------
    # SCORE ROW
    # ----------------------------
    st.markdown("### Score Summary")

    cols = st.columns(6)

    scores = [
        ("Reality", readiness),
        ("Concept", concept),
        ("Financial", financial),
        ("Post-Discovery", post),
        ("Pressure", pressure),
        ("Overall", overall),
    ]

    for col, (label, score) in zip(cols, scores):
        display = "-" if score is None else round(score, 1)
        cls = _metric_class(score)

        with col:
            st.markdown(
                f"""
                <div class="fd-metric {cls}">
                    <div class="fd-metric-label">{label}</div>
                    <div class="fd-metric-value">{display}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ----------------------------
    # OVERALL RESULT
    # ----------------------------
    result_class = _result_class(overall)

    st.markdown(
        f"""
        <div class="fd-featured {result_class}">
            <div class="fd-big">{verdict}</div>
            <div class="fd-subtitle">
                This reflects how the full picture comes together across fit,
                concept quality, financial viability, and deal structure.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------
    # WHAT STANDS OUT
    # ----------------------------
    strengths = _build_high_level_strengths(
        readiness, concept, financial, post, pressure, packet
    )
    risks = _build_high_level_risks(
        readiness, concept, financial, post, pressure, packet
    )

    st.markdown("### What Stands Out")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### What Looks Stronger")
        if strengths:
            for item in strengths:
                st.write(f"- {item}")
        else:
            st.write("- No major strength signals identified yet.")

    with col2:
        st.markdown("#### What May Need Work")
        if risks:
            for item in risks:
                st.write(f"- {item}")
        else:
            st.write("- No major risk signals identified yet.")

    # ----------------------------
    # ENGINE DETAILS
    # ----------------------------
    if packet.get("conditions"):
        st.markdown("### Conditions Before Moving Forward")
        for item in packet["conditions"]:
            st.write(f"- {item}")

    if packet.get("key_risks"):
        st.markdown("### Key Risks")
        for item in packet["key_risks"]:
            st.write(f"- {item}")

    # ----------------------------
    # DECISION ACTION
    # ----------------------------
    st.markdown("---")
    st.markdown("### Final Choice")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Yes — Moving Forward", key="final_yes_forward", use_container_width=True):
            st.session_state["decision_locked"] = True
            st.session_state["final_decision_action"] = "Move Forward"
            st.session_state["move_forward"] = True
            st.session_state["walk_away"] = False
            st.success("Decision recorded: Moving forward with the franchise.")
            st.rerun()

    with c2:
        if st.button("No — Walking Away", key="final_no_walk_away", use_container_width=True):
            st.session_state["decision_locked"] = True
            st.session_state["final_decision_action"] = "Walk Away"
            st.session_state["move_forward"] = False
            st.session_state["walk_away"] = True
            st.warning("Decision recorded: Walking away from the franchise.")
            st.rerun()

    action = st.session_state.get("final_decision_action")
    if action:
        st.info(f"Current recorded decision: {action}")
