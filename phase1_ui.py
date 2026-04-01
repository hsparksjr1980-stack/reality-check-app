import streamlit as st
from phase1_questions import QUESTION_BANK, CATEGORY_META, CATEGORY_WEIGHTS, SCALE_LABELS
from phase1_logic import (
    calculate_total_score,
    get_verdict,
    get_score_color,
    generate_risk_flags,
    get_critical_warnings,
    generate_insights,
    get_meaning_text,
    get_top_drivers,
)
from shared_ui import render_carry_forward_warning

def render_question(question):
    st.markdown(f"**{question['label']}**")
    if question.get("help"):
        st.caption(question["help"])

    option_map = {
        SCALE_LABELS[0]: 0,
        SCALE_LABELS[1]: 1,
        SCALE_LABELS[2]: 2,
        SCALE_LABELS[3]: 3,
        SCALE_LABELS[4]: 4,
    }

    selected_label = st.radio(
        "Select the answer that fits best:",
        options=list(option_map.keys()),
        index=2,
        key=question["id"],
    )
    return option_map[selected_label]

def render_phase_1():
    st.header("Concept Validation")
    st.write("This phase tests whether the concept itself holds up before you waste time on financing, site work, or buildout.")
    st.info("This is not about whether you like the concept. It is about whether the concept survives scrutiny.")

    render_carry_forward_warning()

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

    if st.button("Calculate Concept Validation", type="primary"):
        total_score, category_scores = calculate_total_score(answers)
        verdict = get_verdict(total_score)
        color = get_score_color(total_score)
        flags = generate_risk_flags(answers)
        critical_warnings = get_critical_warnings(answers)
        insights = generate_insights(answers, total_score)
        top_drivers = get_top_drivers(answers, category_scores)
        meaning_text = get_meaning_text(total_score)

        st.session_state["phase_1_answers"] = answers
        st.session_state["phase_1_score"] = total_score
        st.session_state["phase_1_verdict"] = verdict
        st.session_state["phase_1_category_scores"] = category_scores

        st.markdown("---")
        st.subheader("Phase 1 Result")

        st.markdown(
            f"""
            <div style="padding:20px; border-radius:14px; border:1px solid #ddd; background:#fafafa;">
                <div style="font-size:13px; color:#666; margin-bottom:6px;">Concept Validation</div>
                <div style="font-size:34px; font-weight:700; color:{color}; margin-bottom:8px;">{verdict}</div>
                <div style="font-size:22px;"><strong>Score: {total_score} / 100</strong></div>
            </div>
            """,
            unsafe_allow_html=True
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

        st.markdown("### What You Still Need Before Moving On")
        st.write("- Clearer local economics")
        st.write("- Stronger operator validation")
        st.write("- Better proof of franchisor support in your market")
        st.write("- Confidence that the concept works outside the sales pitch")

        st.markdown(
            """
            <div style="padding:18px; border-radius:14px; background:#f6f6f6; border:1px solid #ddd; margin-top:10px;">
                <div style="font-size:24px; font-weight:700; margin-bottom:8px;">Next</div>
                <div style="font-size:16px; margin-bottom:8px;">Move to Financial Model to test whether the deal is actually financeable and whether your capital plan is realistic.</div>
                <div style="font-size:14px; color:#555;">A viable concept can still fail if the capital structure is wrong.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
