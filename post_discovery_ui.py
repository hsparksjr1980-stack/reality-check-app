import streamlit as st
from post_discovery_questions import QUESTION_BANK, CATEGORY_META, CATEGORY_WEIGHTS, SCALE_LABELS
from post_discovery_logic import (
    calculate_total_score,
    get_verdict,
    get_score_color,
    generate_risk_flags,
    get_critical_warnings,
    generate_insights,
    get_meaning_text,
    get_top_drivers,
    get_post_discovery_decision,
)
from shared_ui import render_carry_forward_warning


def render_question(question):
    st.markdown(f"**{question['label']}**")
    if question.get("help"):
        st.caption(question["help"])
    option_map = {SCALE_LABELS[i]: i for i in range(5)}
    selected_label = st.radio(
        "Select the answer that fits best:",
        options=list(option_map.keys()),
        index=2,
        key=question["id"],
    )
    return option_map[selected_label]


def render_framework_block(title, look_at, common, ask, pressure):
    st.markdown(f"### {title}")

    with st.expander("What to Look At"):
        for item in look_at:
            st.write(f"- {item}")

    with st.expander("What’s Common in the Industry"):
        for item in common:
            st.write(f"- {item}")

    with st.expander("What to Ask"):
        for item in ask:
            st.write(f"- {item}")

    with st.expander("Pressure Test"):
        for item in pressure:
            st.write(f"- {item}")


def render_post_discovery():
    st.header("Post-Discovery")
    st.write(
        "This section tests whether Discovery actually improved the facts, "
        "or whether it only increased your momentum toward the deal."
    )
    st.info(
        "This is not about how excited you feel. It is about whether Discovery "
        "gave you enough evidence to move forward responsibly."
    )

    render_carry_forward_warning()

    # -----------------------------------
    # Global framing / PRD alignment
    # -----------------------------------
    render_framework_block(
        "How to Use Post-Discovery",
        look_at=[
            "What you now know about the franchise system",
            "What is still unknown",
            "What your personal exposure really looks like",
            "Whether the economics are becoming more real or still theoretical",
        ],
        common=[
            "Discovery often increases emotional commitment faster than it improves actual certainty",
            "Many buyers leave Discovery with more confidence but not more proof",
            "Big risks often remain unresolved at this stage: no site, no lease, no bids, no real local economics",
        ],
        ask=[
            "Did Discovery actually reduce uncertainty, or just increase momentum?",
            "Do I understand the franchise system better, or do I just feel more comfortable with the people?",
            "What still has not been validated in a way that would matter if the deal goes badly?",
        ],
        pressure=[
            "If nothing improved except confidence, this stage failed",
            "If major unknowns still exist, the decision should stay conditional",
            "If the economics only work under ideal assumptions, you are not actually through Discovery",
        ],
    )

    # -----------------------------------
    # Guardrails / what must be true
    # -----------------------------------
    st.markdown("### Guardrails (What Must Be True)")
    st.caption("Set minimum standards the deal must meet before you go further.")

    g1, g2, g3, g4 = st.columns(4)
    with g1:
        max_rent_pct = st.number_input(
            "Max Rent % of Revenue",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.get("pd_max_rent_pct", 10.0)),
            step=0.5,
            key="pd_max_rent_pct_input",
        )
    with g2:
        max_buildout = st.number_input(
            "Max Buildout",
            min_value=0.0,
            value=float(st.session_state.get("pd_max_buildout", 400000.0)),
            step=5000.0,
            key="pd_max_buildout_input",
        )
    with g3:
        min_liquidity = st.number_input(
            "Min Liquidity Required",
            min_value=0.0,
            value=float(st.session_state.get("pd_min_liquidity", 100000.0)),
            step=5000.0,
            key="pd_min_liquidity_input",
        )
    with g4:
        min_target_revenue = st.number_input(
            "Min Revenue Target",
            min_value=0.0,
            value=float(st.session_state.get("pd_min_target_revenue", 0.0)),
            step=5000.0,
            key="pd_min_target_revenue_input",
        )

    st.session_state["pd_max_rent_pct"] = float(max_rent_pct)
    st.session_state["pd_max_buildout"] = float(max_buildout)
    st.session_state["pd_min_liquidity"] = float(min_liquidity)
    st.session_state["pd_min_target_revenue"] = float(min_target_revenue)

    # -----------------------------------
    # Unknowns & gaps
    # -----------------------------------
    st.markdown("### Unknowns & Gaps")
    st.caption("These are the things that often still remain unresolved after Discovery.")

    u1, u2, u3, u4 = st.columns(4)
    with u1:
        no_site_selected = st.checkbox(
            "No site selected",
            value=st.session_state.get("pd_no_site_selected", False),
            key="pd_no_site_selected_input",
        )
    with u2:
        no_lease = st.checkbox(
            "No lease negotiated",
            value=st.session_state.get("pd_no_lease", False),
            key="pd_no_lease_input",
        )
    with u3:
        no_bids = st.checkbox(
            "No contractor bids",
            value=st.session_state.get("pd_no_bids", False),
            key="pd_no_bids_input",
        )
    with u4:
        no_final_costs = st.checkbox(
            "No finalized costs",
            value=st.session_state.get("pd_no_final_costs", False),
            key="pd_no_final_costs_input",
        )

    st.session_state["pd_no_site_selected"] = no_site_selected
    st.session_state["pd_no_lease"] = no_lease
    st.session_state["pd_no_bids"] = no_bids
    st.session_state["pd_no_final_costs"] = no_final_costs

    unknown_count = sum([no_site_selected, no_lease, no_bids, no_final_costs])

    if unknown_count >= 3:
        st.error("You still have several major unknowns unresolved.")
    elif unknown_count >= 1:
        st.warning("You still have important gaps that should keep your decision conditional.")
    else:
        st.success("Your major Discovery-stage unknowns appear more controlled.")

    # -----------------------------------
    # Question bank scoring
    # -----------------------------------
    answers = {}
    total_questions = sum(len(v) for v in QUESTION_BANK.values())
    answered_count = 0

    for category_key, questions in QUESTION_BANK.items():
        meta = CATEGORY_META[category_key]
        with st.expander(meta["title"], expanded=True):
            st.write(meta["intro"])
            for q in questions:
                answers[q["id"]] = render_question(q)
                answered_count += 1
                st.markdown("---")

    st.progress(answered_count / total_questions)
    st.caption(f"{answered_count} of {total_questions} questions completed")

    if st.button("Calculate Post-Discovery", type="primary"):
        total_score, category_scores = calculate_total_score(answers)
        verdict = get_verdict(total_score)
        color = get_score_color(total_score)
        flags = generate_risk_flags(answers)
        critical_warnings = get_critical_warnings(answers)
        insights = generate_insights(answers, total_score)
        top_drivers = get_top_drivers(answers, category_scores)
        meaning_text = get_meaning_text(total_score)
        move_forward_decision = get_post_discovery_decision(total_score, answers)

        # apply extra penalties for unresolved gaps
        gap_penalty = 0
        if no_site_selected:
            gap_penalty += 3
        if no_lease:
            gap_penalty += 3
        if no_bids:
            gap_penalty += 2
        if no_final_costs:
            gap_penalty += 2

        adjusted_score = max(total_score - gap_penalty, 0)

        # strengthen decision if too many unknowns remain
        final_post_discovery_decision = move_forward_decision["verdict"]
        if unknown_count >= 3:
            final_post_discovery_decision = "Do Not Proceed"
        elif unknown_count >= 1 and move_forward_decision["verdict"] == "Proceed":
            final_post_discovery_decision = "Proceed with Conditions"

        st.session_state["post_discovery_answers"] = answers
        st.session_state["post_discovery_score"] = adjusted_score
        st.session_state["post_discovery_raw_score"] = total_score
        st.session_state["post_discovery_verdict"] = verdict
        st.session_state["post_discovery_category_scores"] = category_scores
        st.session_state["post_discovery_decision"] = final_post_discovery_decision
        st.session_state["post_discovery_unknown_count"] = unknown_count

        st.markdown("---")
        st.subheader("Post-Discovery Result")
        st.markdown(
            f"""
            <div class="rc-card">
                <div class="rc-kicker">Post-Discovery</div>
                <div style="font-size:34px; font-weight:700; color:{color}; margin-bottom:8px;">{verdict}</div>
                <div style="font-size:22px;"><strong>Score: {adjusted_score} / 100</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if gap_penalty > 0:
            st.warning(
                f"Your score was reduced by {gap_penalty} points because key unknowns still remain unresolved."
            )

        if critical_warnings:
            st.markdown("### Critical Warnings")
            for warning in critical_warnings:
                st.error(warning)

        st.markdown("### What This Result Says")
        for line in meaning_text:
            st.write(f"- {line}")

        st.markdown("### Main Drivers")
        if top_drivers["weak_categories"]:
            st.write("**Weakest categories:**")
            for item in top_drivers["weak_categories"]:
                st.write(f"- {item['label']} ({item['score_text']})")
        if top_drivers["weak_answers"]:
            st.write("**Answers driving risk most:**")
            for item in top_drivers["weak_answers"]:
                st.write(f"- {item['label']} — {item['category']}")

        st.markdown("### Score by Category")
        for category_key, details in category_scores.items():
            max_weight = CATEGORY_WEIGHTS[category_key]
            label = CATEGORY_META[category_key]["title"]
            weighted = details["weighted_score"]
            st.write(f"**{label}** — {weighted} / {max_weight}")
            st.progress(min(weighted / max_weight, 1.0))

        st.markdown("### Biggest Risk Factors")
        for flag in flags:
            st.markdown(f"**{flag['title']}**")
            st.write(flag["description"])
            st.write(f"**Impact:** {flag['impact']}")
            st.markdown("---")

        st.markdown("### What This Means Specifically")
        for insight in insights:
            st.write(f"- {insight}")

        st.markdown("### What Must Be True Before You Move Forward")
        st.write(f"- All-in rent should stay at or below **{max_rent_pct:.1f}%** of revenue")
        st.write(f"- Buildout should stay at or below **{money(max_buildout)}**" if 'money' in globals() else f"- Buildout should stay at or below **${max_buildout:,.0f}**")
        st.write(f"- You should maintain at least **${min_liquidity:,.0f}** of liquidity")
        if min_target_revenue > 0:
            st.write(f"- The deal should credibly support at least **${min_target_revenue:,.0f}** in target revenue")

        st.markdown("### Decision: Move Forward After Discovery?")
        decision_color = (
            "#B00020" if final_post_discovery_decision == "Do Not Proceed"
            else "#C76A00" if final_post_discovery_decision == "Proceed with Conditions"
            else "#2E7D32"
        )

        if final_post_discovery_decision == "Do Not Proceed":
            decision_summary = "Too many key risks or unknowns remain unresolved to justify moving forward."
            next_step = "Do not advance until the missing economics, site, lease, and buildout realities are materially clearer."
        elif final_post_discovery_decision == "Proceed with Conditions":
            decision_summary = "There may be a path forward, but only if the remaining gaps are resolved first."
            next_step = "Move forward only with explicit guardrails and specific unresolved issues tracked."
        else:
            decision_summary = "Discovery appears to have improved the facts enough to justify moving to the next stage."
            next_step = "Advance, but keep pressure-testing economics, site quality, and execution risk."

        st.markdown(
            f"""
            <div class="rc-card-soft">
                <div class="rc-kicker">Post-Discovery Decision</div>
                <div style="font-size:30px; font-weight:700; color:{decision_color}; margin-bottom:8px;">
                    {final_post_discovery_decision}
                </div>
                <div class="rc-muted" style="font-size:15px; margin-bottom:10px;">
                    {decision_summary}
                </div>
                <div style="font-weight:600; color:#23467F; margin-bottom:6px;">Next Step</div>
                <div style="color:#1F2937;">{next_step}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### What This Decision Really Means")
        st.write("- Discovery should reduce uncertainty, not just increase confidence.")
        st.write("- If the economics are still theoretical, the deal is not actually validated yet.")
        st.write("- If major unknowns still exist, your next step should be conditional, not emotional.")

        st.markdown("### What You Still Need Before Committing Further")
        if no_site_selected:
            st.write("- A real site, not a hypothetical site")
        if no_lease:
            st.write("- Actual lease economics and exposure")
        if no_bids:
            st.write("- Contractor or buildout pricing grounded in real bids")
        if no_final_costs:
            st.write("- More confidence in final startup cost range")
        st.write("- Confidence that Discovery improved the facts, not just the momentum")
