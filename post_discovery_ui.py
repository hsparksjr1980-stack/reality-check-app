import streamlit as st
from post_discovery_questions import QUESTION_BANK, CATEGORY_META, CATEGORY_WEIGHTS, SCALE_LABELS
from post_discovery_logic import (
    calculate_total_score, get_verdict, get_score_color, generate_risk_flags,
    get_critical_warnings, generate_insights, get_meaning_text, get_top_drivers,
    get_post_discovery_decision,
)
from shared_ui import render_carry_forward_warning

def render_question(question):
    st.markdown(f"**{question['label']}**")
    if question.get("help"):
        st.caption(question["help"])
    option_map = {SCALE_LABELS[i]: i for i in range(5)}
    selected_label = st.radio("Select the answer that fits best:", options=list(option_map.keys()), index=2, key=question["id"])
    return option_map[selected_label]

def render_post_discovery():
    st.header("Post-Discovery Review")
    st.write("This section tests whether Discovery actually validated the opportunity or simply increased your momentum toward the deal.")
    st.info("This is not about how excited you feel. It is about whether Discovery improved the evidence enough to keep going.")
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

    if st.button("Calculate Post-Discovery Review", type="primary"):
        total_score, category_scores = calculate_total_score(answers)
        verdict = get_verdict(total_score)
        color = get_score_color(total_score)
        flags = generate_risk_flags(answers)
        critical_warnings = get_critical_warnings(answers)
        insights = generate_insights(answers, total_score)
        top_drivers = get_top_drivers(answers, category_scores)
        meaning_text = get_meaning_text(total_score)
        move_forward_decision = get_post_discovery_decision(total_score, answers)

        st.session_state["post_discovery_answers"] = answers
        st.session_state["post_discovery_score"] = total_score
        st.session_state["post_discovery_verdict"] = verdict
        st.session_state["post_discovery_category_scores"] = category_scores
        st.session_state["post_discovery_decision"] = move_forward_decision["verdict"]

        st.markdown("---")
        st.subheader("Post-Discovery Result")
        st.markdown(f"""
            <div class="rc-card">
                <div class="rc-kicker">Post-Discovery Review</div>
                <div style="font-size:34px; font-weight:700; color:{color}; margin-bottom:8px;">{verdict}</div>
                <div style="font-size:22px;"><strong>Score: {total_score} / 100</strong></div>
            </div>
            """, unsafe_allow_html=True)

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

        st.markdown("### Decision: Move Forward After Discovery?")
        st.markdown(f"""
            <div class="rc-card-soft">
                <div class="rc-kicker">Post-Discovery Decision</div>
                <div style="font-size:30px; font-weight:700; color:{move_forward_decision['color']}; margin-bottom:8px;">
                    {move_forward_decision['verdict']}
                </div>
                <div class="rc-muted" style="font-size:15px; margin-bottom:10px;">
                    {move_forward_decision['summary']}
                </div>
                <div style="font-weight:600; color:#23467F; margin-bottom:6px;">Next Step</div>
                <div style="color:#1F2937;">{move_forward_decision['next_step']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### What This Decision Really Means")
        for item in move_forward_decision["what_this_decision_really_means"]:
            st.write(f"- {item}")

        st.markdown("### What You Still Need Before Committing Further")
        st.write("- Clearer economic confirmation")
        st.write("- Stronger trust in the support model")
        st.write("- Confidence that Discovery improved the facts, not just the momentum")
        st.write("- Evidence that the deal deserves deeper financial pressure-testing")
